"""
books/views.py
Campus Secondhand Book Trading Platform — Views
校园二手书交易平台 — 视图层
"""
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.cache import cache
from django.http import JsonResponse

from .models import Book, University, Message as ChatMessage, Advertisement, Sponsor, BookImage, College, Major, Order
from .forms import BookForm

logger = logging.getLogger('books')


def _college_suggestions_json():
    """
    Return a dict {str(university_pk): [college_name, ...]} for all universities.
    用于模板中动态填充学院下拉建议。
    Used by templates to populate college suggestions dynamically.
    """
    import json
    suggestions = {}
    for col in College.objects.select_related('university').order_by('university_id', 'name'):
        key = str(col.university_id)
        suggestions.setdefault(key, []).append(col.name)
    return json.dumps(suggestions)


# ──────────────────────────────────────────────
# Home / 主页
# ──────────────────────────────────────────────
def home(request):
    """
    主页书单视图 / Home book-listing view.
    支持按学校-学院-专业-年级-课程多维筛选。
    Supports multi-dimensional filtering: university, college, grade, category, course, search.
    """
    # 获取查询参数 / Get filter parameters
    # university default logic:
    #   - explicit ?university=all  → show all
    #   - explicit ?university=X    → use X
    #   - not in URL at all         → use user's profile university, else UrFU
    raw_uni = request.GET.get('university', None)
    if raw_uni is None:
        # No explicit selection — resolve default from profile or UrFU
        university_id = ''
        if request.user.is_authenticated:
            try:
                uid = request.user.profile.university_id
                if uid:
                    university_id = str(uid)
            except Exception:
                pass
        if not university_id:
            _urfu = University.objects.filter(is_featured=True).first()
            university_id = str(_urfu.pk) if _urfu else ''
    elif raw_uni == 'all':
        university_id = ''
    else:
        university_id = raw_uni.strip()

    college   = request.GET.get('college',    '').strip()
    major     = request.GET.get('major',      '').strip()
    category  = request.GET.get('category',   '').strip()
    grade     = request.GET.get('grade',      '').strip()
    search    = request.GET.get('search',     '').strip()
    price_sort = request.GET.get('price_sort', '').strip()
    sort_by   = request.GET.get('sort', 'newest').strip()
    page_number = request.GET.get('page', 1)

    # 只显示未售出的书 / Only show unsold books
    books_qs = Book.objects.filter(is_sold=False).select_related('seller', 'university')

    # 逐级筛选 / Apply filters progressively
    if university_id:
        books_qs = books_qs.filter(university_id=university_id)
    if college:
        books_qs = books_qs.filter(college__icontains=college)
    if major:
        books_qs = books_qs.filter(program__icontains=major)
    if category:
        books_qs = books_qs.filter(category=category)
    if grade:
        books_qs = books_qs.filter(grade=grade)
    if search:
        books_qs = books_qs.filter(
            Q(title__icontains=search)
            | Q(author__icontains=search)
            | Q(course__icontains=search)
        )

    if sort_by == 'oldest':
        books_qs = books_qs.order_by('created_at')
    if price_sort == 'asc':
        books_qs = books_qs.order_by('price')
    elif price_sort == 'desc':
        books_qs = books_qs.order_by('-price')

    # 缓存大学列表 / Cache universities
    universities = cache.get('all_universities')
    if universities is None:
        universities = list(University.objects.all())
        cache.set('all_universities', universities, 3600)

    active_ads = [ad for ad in Advertisement.objects.filter(is_active=True)[:3] if ad.is_visible]
    active_sponsors = list(Sponsor.objects.filter(is_active=True)[:6])

    paginator = Paginator(books_qs, 12)
    page_obj = paginator.get_page(page_number)
    cart = request.session.get('cart', [])

    logger.info(
        'Home: search=%r uni=%r college=%r major=%r grade=%r → %d results',
        search, university_id, college, major, grade, paginator.count,
    )

    # 服务端渲染学院列表 / Server-side college list for selected university
    selected_uni_colleges = []
    if university_id:
        selected_uni_colleges = list(
            College.objects.filter(university_id=university_id)
                           .values_list('name', flat=True)
                           .order_by('name')
        )

    # 服务端渲染专业列表 / Server-side major list for selected college
    selected_col_majors = []
    if college and university_id:
        try:
            col_obj = College.objects.get(university_id=university_id, name__iexact=college)
            selected_col_majors = list(
                col_obj.majors.values_list('name', flat=True).order_by('name')
            )
        except College.DoesNotExist:
            pass

    context = {
        'page_obj': page_obj,
        'universities': universities,
        'categories': Book.CATEGORY_CHOICES,
        'grades': Book.GRADE_CHOICES,
        'selected_university': university_id,
        'selected_college': college,
        'selected_major': major,
        'selected_category': category,
        'selected_grade': grade,
        'search': search,
        'price_sort': price_sort,
        'sort_by': sort_by,
        'active_ads': active_ads,
        'active_sponsors': active_sponsors,
        'cart_count': len(cart),
        'selected_uni_colleges': selected_uni_colleges,
        'selected_col_majors': selected_col_majors,
        'college_suggestions_json': _college_suggestions_json(),
    }
    return render(request, 'home.html', context)


# ──────────────────────────────────────────────
# Book Detail / 书籍详情
# ──────────────────────────────────────────────
def book_detail(request, pk):
    """书籍详情页 / Book detail page"""
    book = get_object_or_404(
        Book.objects.select_related('seller', 'seller__profile', 'university'),
        pk=pk
    )
    is_owner = request.user.is_authenticated and request.user == book.seller

    # 购物车状态 / Cart state
    cart = request.session.get('cart', [])
    in_cart = pk in cart

    logger.info('Book detail: pk=%d by %s', pk, request.user)
    return render(request, 'detail.html', {
        'book': book,
        'is_owner': is_owner,
        'in_cart': in_cart,
        'cart_count': len(cart),
    })


# ──────────────────────────────────────────────
# Create / Edit / Delete Book / 上架/编辑/删除
# ──────────────────────────────────────────────
@login_required
def create_book(request):
    """上架新书 / List a new book for sale"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            _save_extra_images(request, book)
            cache.delete('all_universities')
            messages.success(request, 'Your book has been listed successfully!')
            logger.info('Book created: "%s" by %s', book.title, request.user.username)
            return redirect('books:detail', pk=book.pk)
    else:
        # 预填用户资料里的学校和学院 / Pre-fill from user profile
        initial = {}
        try:
            profile = request.user.profile
            if profile.university_id:
                initial['university'] = profile.university_id
            if profile.college:
                initial['college'] = profile.college
        except Exception:
            pass
        form = BookForm(initial=initial)
    return render(request, 'sell.html', {
        'form': form,
        'action': 'Create',
        'college_suggestions_json': _college_suggestions_json(),
    })


@login_required
def edit_book(request, pk):
    """编辑书籍信息 / Edit an existing book listing"""
    book = get_object_or_404(Book, pk=pk, seller=request.user)

    # 删除单张额外图片 / Delete a single extra image via ?delete_img=<id>
    delete_img_id = request.GET.get('delete_img')
    if delete_img_id:
        BookImage.objects.filter(pk=delete_img_id, book=book).delete()
        return redirect('books:edit', pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            _save_extra_images(request, book)
            messages.success(request, 'Book updated.')
            logger.info('Book edited: pk=%d by %s', pk, request.user.username)
            return redirect('books:detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'sell.html', {
        'form': form, 'book': book, 'action': 'Edit',
        'college_suggestions_json': _college_suggestions_json(),
    })


def _save_extra_images(request, book):
    """保存多张额外图片到 BookImage 表 / Save multiple extra photos to BookImage"""
    for img_file in request.FILES.getlist('extra_images'):
        BookImage.objects.create(book=book, image=img_file)


@login_required
def delete_book(request, pk):
    """删除书籍 / Delete a book listing"""
    book = get_object_or_404(Book, pk=pk, seller=request.user)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'"{title}" has been removed. / 已删除。')
        logger.info('Book deleted: "%s" by %s', title, request.user.username)
    return redirect('users:profile')


# ──────────────────────────────────────────────
# Shopping Cart / 购物车
# ──────────────────────────────────────────────
def cart_view(request):
    """
    购物车页面 / Shopping cart page.
    Session-based cart: stores list of book PKs.
    基于 Session 存储购物车书籍 ID 列表。
    """
    cart = request.session.get('cart', [])
    # 查询购物车中的书籍（过滤已售出）/ Fetch cart books (exclude sold)
    cart_books = list(Book.objects.filter(pk__in=cart, is_sold=False).select_related('university'))
    # 保持购物车中只包含存在且未售出的书 / Clean up invalid entries
    valid_pks = [b.pk for b in cart_books]
    if set(valid_pks) != set(cart):
        request.session['cart'] = valid_pks

    # 计算总价和平台费 / Calculate totals
    subtotal = sum(float(b.price) for b in cart_books if b.price)
    platform_fee = round(subtotal * 0.05, 2)
    total = round(subtotal + platform_fee, 2)

    return render(request, 'cart.html', {
        'cart_books': cart_books,
        'subtotal': subtotal,
        'platform_fee': platform_fee,
        'total': total,
        'cart_count': len(valid_pks),
    })


@login_required
def add_to_cart(request, pk):
    """
    添加书籍到购物车 / Add a book to the cart.
    Supports both regular POST and AJAX (X-Requested-With header).
    支持普通提交和 AJAX 请求。
    """
    book = get_object_or_404(Book, pk=pk, is_sold=False)
    cart = request.session.get('cart', [])

    if pk not in cart:
        cart.append(pk)
        request.session['cart'] = cart
        request.session.modified = True
        msg = f'"{book.title}" added to cart. / 已加入购物车。'
    else:
        msg = f'"{book.title}" is already in your cart. / 已在购物车中。'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'count': len(cart), 'message': msg})
    messages.success(request, msg)
    # 返回来源页 / Redirect back to referrer
    return redirect(request.META.get('HTTP_REFERER', 'books:home'))


@login_required
def remove_from_cart(request, pk):
    """从购物车移除书籍 / Remove a book from the cart"""
    cart = request.session.get('cart', [])
    if pk in cart:
        cart.remove(pk)
        request.session['cart'] = cart
        request.session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'count': len(cart)})
    return redirect('books:cart')


@login_required
def clear_cart(request):
    """清空购物车 / Clear the entire cart"""
    request.session['cart'] = []
    request.session.modified = True
    messages.success(request, 'Cart cleared. / 购物车已清空。')
    return redirect('books:cart')


# ──────────────────────────────────────────────
# Chat / 站内聊天
# ──────────────────────────────────────────────
@login_required
def chat_view(request, user_id=None):
    """
    站内聊天视图 / In-platform chat view.
    显示所有会话列表，可选择查看某用户的具体聊天记录。
    Shows all conversations, with an optional active conversation.
    """
    from django.contrib.auth.models import User

    # 找到曾有过聊天的用户 / Find all users this user has chatted with
    sent_to = ChatMessage.objects.filter(sender=request.user).values_list('receiver_id', flat=True).distinct()
    received_from = ChatMessage.objects.filter(receiver=request.user).values_list('sender_id', flat=True).distinct()
    conversation_user_ids = set(sent_to) | set(received_from)
    conversation_users = User.objects.filter(pk__in=conversation_user_ids).exclude(pk=request.user.pk)

    other_user = None
    conversation = []
    book_context = None

    if user_id:
        other_user = get_object_or_404(User, pk=user_id)
        book_id = request.GET.get('book')
        if book_id:
            book_context = Book.objects.filter(pk=book_id).first()

        if request.method == 'POST':
            text = request.POST.get('text', '').strip()
            if text:
                msg = ChatMessage.objects.create(
                    sender=request.user,
                    receiver=other_user,
                    book=book_context,
                    text=text,
                )
                logger.info('Message: %s → %s', request.user.username, other_user.username)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'id': msg.pk,
                        'text': msg.text,
                        'time': msg.created_at.strftime('%H:%M'),
                    })
                return redirect('books:chat_user', user_id=user_id)

        # 将消息标记为已读 / Mark incoming messages as read
        ChatMessage.objects.filter(
            sender=other_user, receiver=request.user, is_read=False
        ).update(is_read=True)

        conversation = ChatMessage.objects.filter(
            Q(sender=request.user, receiver=other_user)
            | Q(sender=other_user, receiver=request.user)
        ).select_related('sender').order_by('created_at')

        if other_user not in conversation_users:
            conversation_users = list(conversation_users) + [other_user]

    context = {
        'conversation_users': conversation_users,
        'other_user': other_user,
        'conversation': conversation,
        'book_context': book_context,
        'cart_count': len(request.session.get('cart', [])),
    }
    return render(request, 'chat.html', context)


def api_messages_poll(request, user_id):
    """AJAX 消息轮询端点 / AJAX endpoint to poll new messages"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'unauthenticated'}, status=401)
    from django.contrib.auth.models import User
    other_user = get_object_or_404(User, pk=user_id)
    since_id = request.GET.get('since', 0)
    msgs = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other_user)
        | Q(sender=other_user, receiver=request.user),
        pk__gt=since_id,
    ).order_by('created_at')
    data = [
        {
            'id': m.pk,
            'text': m.text,
            'mine': m.sender_id == request.user.pk,
            'time': m.created_at.strftime('%H:%M'),
        }
        for m in msgs
    ]
    return JsonResponse({'messages': data})


# ──────────────────────────────────────────────
# Checkout / 结账下单
# ──────────────────────────────────────────────
@login_required
def checkout_view(request):
    """
    结账视图：将购物车里的书全部生成订单，并标记为已售。
    Creates one Order per cart book, marks books as sold, then clears the cart.
    """
    cart = request.session.get('cart', [])
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('books:cart')

    # Only include books that are still available and not owned by the buyer
    cart_books = list(
        Book.objects.filter(pk__in=cart, is_sold=False)
                    .exclude(seller=request.user)
                    .select_related('seller', 'university')
    )

    if not cart_books:
        messages.warning(request, 'No available books to order (items may be sold or belong to you).')
        request.session['cart'] = []
        return redirect('books:cart')

    if request.method == 'POST':
        created_orders = []
        for book in cart_books:
            order = Order.objects.create(
                book=book,
                buyer=request.user,
                seller=book.seller,
                status='pending',
            )
            # Mark as sold
            book.is_sold = True
            book.save(update_fields=['is_sold'])
            created_orders.append(order)

        # Clear cart
        request.session['cart'] = []
        request.session.modified = True

        logger.info(
            'Checkout: %s placed %d order(s)', request.user.username, len(created_orders)
        )
        messages.success(
            request,
            f'Order placed successfully! {len(created_orders)} book(s) purchased. '
            'Contact each seller to arrange delivery.'
        )
        return redirect('books:orders')

    # GET: preview the order
    subtotal = sum(float(b.price) for b in cart_books if b.price)
    platform_fee = round(subtotal * 0.05, 2)
    total = round(subtotal + platform_fee, 2)

    skipped = len(cart) - len(cart_books)

    return render(request, 'checkout.html', {
        'cart_books': cart_books,
        'subtotal': subtotal,
        'platform_fee': platform_fee,
        'total': total,
        'skipped': skipped,
        'cart_count': len(cart_books),
    })


@login_required
def orders_view(request):
    """
    订单列表页：展示买家的采购订单和卖家的销售订单。
    Shows buyer's purchases and seller's sales.
    """
    purchases = (
        Order.objects.filter(buyer=request.user)
                     .select_related('book', 'book__university', 'seller')
                     .order_by('-created_at')
    )
    sales = (
        Order.objects.filter(seller=request.user)
                     .select_related('book', 'book__university', 'buyer')
                     .order_by('-created_at')
    )
    return render(request, 'orders.html', {
        'purchases': purchases,
        'sales': sales,
        'cart_count': len(request.session.get('cart', [])),
    })


# ──────────────────────────────────────────────
# Mark as Sold / 标记已售
# ──────────────────────────────────────────────
@login_required
def mark_sold(request, pk):
    """卖家将书标记为已售 / Seller marks a book as sold"""
    book = get_object_or_404(Book, pk=pk, seller=request.user)
    if request.method == 'POST':
        book.is_sold = not book.is_sold
        book.save(update_fields=['is_sold'])
        status = 'sold' if book.is_sold else 'available'
        messages.success(request, f'"{book.title}" marked as {status}.')
        logger.info('Mark sold: pk=%d is_sold=%s by %s', pk, book.is_sold, request.user.username)
    return redirect(request.META.get('HTTP_REFERER', 'users:profile'))


# ──────────────────────────────────────────────
# AJAX: Cascading dropdowns (university → college → major)
# 级联下拉：大学 → 学院 → 专业
# ──────────────────────────────────────────────
def api_colleges(request):
    uni_id = request.GET.get('university_id')
    if not uni_id:
        return JsonResponse({'colleges': []})
    colleges = list(
        College.objects.filter(university_id=uni_id)
        .order_by('name')
        .values('id', 'name')
    )
    return JsonResponse({'colleges': colleges})


def api_majors(request):
    college_id = request.GET.get('college_id')
    if not college_id:
        return JsonResponse({'majors': []})
    majors = list(
        Major.objects.filter(college_id=college_id)
        .order_by('name')
        .values('id', 'name')
    )
    return JsonResponse({'majors': majors})
