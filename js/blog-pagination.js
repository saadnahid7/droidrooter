// Blog Pagination and Category Filtering
document.addEventListener('DOMContentLoaded', function() {
    const categoryFilters = document.querySelectorAll('.category-filter');
    const blogPosts = document.querySelectorAll('.blog-post');
    const pageButtons = document.querySelectorAll('.page-btn');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const articlesInfo = document.getElementById('articles-info');
    
    let currentPage = 1;
    let currentCategory = 'all';
    const postsPerPage = 4;
    
    // Function to show posts for current page and category
    function showPosts() {
        let visiblePosts = [];
        
        // Filter posts by category
        blogPosts.forEach(post => {
            const postCategory = post.getAttribute('data-category');
            if (currentCategory === 'all' || postCategory === currentCategory) {
                visiblePosts.push(post);
            }
        });
        
        // Hide all posts first
        blogPosts.forEach(post => {
            post.style.display = 'none';
        });
        
        // Show posts for current page
        const startIndex = (currentPage - 1) * postsPerPage;
        const endIndex = startIndex + postsPerPage;
        const postsToShow = visiblePosts.slice(startIndex, endIndex);
        
        postsToShow.forEach(post => {
            post.style.display = 'block';
        });
        
        // Update pagination controls
        updatePaginationControls(visiblePosts.length);
        
        // Update articles info
        const totalPosts = visiblePosts.length;
        const showingStart = Math.min(startIndex + 1, totalPosts);
        const showingEnd = Math.min(endIndex, totalPosts);
        articlesInfo.textContent = `Showing ${showingStart}-${showingEnd} of ${totalPosts} articles`;
    }
    
    // Function to update pagination controls
    function updatePaginationControls(totalPosts) {
        const totalPages = Math.ceil(totalPosts / postsPerPage);
        
        // Update page buttons
        pageButtons.forEach(btn => {
            const page = parseInt(btn.getAttribute('data-page'));
            if (page <= totalPages) {
                btn.style.display = 'block';
                if (page === currentPage) {
                    btn.classList.remove('bg-gray-200', 'text-gray-700');
                    btn.classList.add('bg-blue-600', 'text-white');
                } else {
                    btn.classList.remove('bg-blue-600', 'text-white');
                    btn.classList.add('bg-gray-200', 'text-gray-700');
                }
            } else {
                btn.style.display = 'none';
            }
        });
        
        // Update prev/next buttons
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages || totalPages === 0;
        
        // Hide pagination if only one page
        const paginationControls = document.getElementById('pagination-controls');
        if (totalPages <= 1) {
            paginationControls.style.display = 'none';
        } else {
            paginationControls.style.display = 'flex';
        }
    }
    
    // Category filter event listeners
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', function() {
            currentCategory = this.getAttribute('data-category');
            currentPage = 1; // Reset to first page when changing category
            
            // Update active filter
            categoryFilters.forEach(f => {
                f.classList.remove('bg-blue-600', 'text-white');
                f.classList.add('bg-gray-200', 'text-gray-700');
            });
            this.classList.remove('bg-gray-200', 'text-gray-700');
            this.classList.add('bg-blue-600', 'text-white');
            
            showPosts();
        });
    });
    
    // Page button event listeners
    pageButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            currentPage = parseInt(this.getAttribute('data-page'));
            showPosts();
        });
    });
    
    // Previous/Next button event listeners
    prevButton.addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            showPosts();
        }
    });
    
    nextButton.addEventListener('click', function() {
        const totalPosts = Array.from(blogPosts).filter(post => {
            const postCategory = post.getAttribute('data-category');
            return currentCategory === 'all' || postCategory === currentCategory;
        }).length;
        const totalPages = Math.ceil(totalPosts / postsPerPage);
        
        if (currentPage < totalPages) {
            currentPage++;
            showPosts();
        }
    });
    
    // Initialize
    showPosts();
});
