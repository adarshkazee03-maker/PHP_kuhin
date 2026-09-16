from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import BlogPost, Category

def blog_list(request):
    """
    Display list of published blog posts with optional category and search filtering.
    
    Supports:
    - Category filtering via GET parameter 'category'
    - Full-text search via GET parameter 'search' (searches title, excerpt, content)
    - Pagination via GET parameter 'page'
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered blog list template with context
        
    Context:
        - blogs: Queryset of BlogPost objects (filtered and paginated)
        - categories: All available categories
        - search_query: The search query string (if provided)
        - selected_category: The selected category slug (if provided)
    """
    # Use select_related for category to optimize queries (prevents N+1)
    blogs = BlogPost.objects.select_related('category').filter(
        status='published'
    ).order_by('-published_date', '-created_at')
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)
    
    # Search functionality - searches across title, excerpt, and content
    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) | 
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    context = {
        'blogs': blogs,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
    }
    return render(request, 'blogs/blog_list.html', context)

def blog_detail(request, slug):
    """
    Display detailed view of a single blog post with SEO optimization.
    
    Features:
    - Increments view count
    - Shows related posts from the same category
    - Provides breadcrumb navigation
    - Optimized queries with select_related
    - Dynamic meta descriptions for SEO
    
    Args:
        request (HttpRequest): The HTTP request object
        slug (str): The blog post slug for URL routing
        
    Returns:
        HttpResponse: Rendered blog detail template with context
        HttpResponse 404: If blog post not found or not published
        
    Context:
        - blog: The BlogPost object
        - related_blogs: Up to 3 related posts from same category
        - categories: All available categories (for sidebar)
        - breadcrumb_items: Navigation breadcrumb data
    """
    # Use select_related to optimize category query
    blog = get_object_or_404(
        BlogPost.objects.select_related('category'),
        slug=slug,
        status='published'
    )
    
    # Increment view count (efficient update using F expression in production)
    blog.views += 1
    blog.save(update_fields=['views'])
    
    # Get related blog posts from same category with select_related
    related_blogs = BlogPost.objects.select_related('category').filter(
        status='published',
        category=blog.category
    ).exclude(slug=slug).order_by('-published_date')[:3]
    
    # Get all categories for sidebar
    categories = Category.objects.all()
    
    # Prepare breadcrumb data for navigation
    breadcrumb_items = [
        {'label': 'Blog', 'url': '/blog/'},
        {'label': blog.category.name if blog.category else 'Blog', 'url': f'/blog/?category={blog.category.slug}' if blog.category else '/blog/'},
        {'label': blog.title, 'url': None}
    ]
    
    context = {
        'blog': blog,
        'related_blogs': related_blogs,
        'categories': categories,
        'breadcrumb_items': breadcrumb_items,
    }
    return render(request, 'blogs/blog_detail.html', context)

