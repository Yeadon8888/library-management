// 通用函数
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // 5秒后自动消失
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// 密码强度检查
function checkPasswordStrength(password) {
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const isLongEnough = password.length >= 8;
    
    return hasUpperCase && hasLowerCase && hasNumbers && isLongEnough;
}

// 表单验证
document.addEventListener('DOMContentLoaded', function() {
    // 注册表单验证
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = this.querySelector('input[name="password"]').value;
            if (!checkPasswordStrength(password)) {
                e.preventDefault();
                showAlert('密码必须包含大小写字母和数字，且长度不少于8位', 'danger');
            }
        });
    }
    
    // 图书搜索表单
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="q"]');
        const categorySelect = searchForm.querySelector('select[name="category"]');
        
        // 实时搜索（可选）
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                searchForm.submit();
            }, 500);
        });
        
        categorySelect.addEventListener('change', function() {
            searchForm.submit();
        });
    }
});

// 评分系统
function initRatingSystem() {
    const ratingSelect = document.querySelector('select[name="rating"]');
    if (ratingSelect) {
        ratingSelect.addEventListener('change', function() {
            const stars = '⭐'.repeat(this.value);
            this.nextElementSibling.textContent = stars;
        });
    }
}

// 确认删除对话框
function confirmDelete(event, bookTitle) {
    if (!confirm(`确定要删除《${bookTitle}》吗？此操作不可撤销。`)) {
        event.preventDefault();
    }
}

// 添加图书表单验证
function validateBookForm() {
    const form = document.querySelector('form[action*="book/add"]');
    if (form) {
        form.addEventListener('submit', function(e) {
            // ISBN验证
            const isbn = form.querySelector('#isbn').value;
            const isbnRegex = /^(?:\d{10}|\d{13})$/;
            if (!isbnRegex.test(isbn)) {
                e.preventDefault();
                showAlert('ISBN必须是10位或13位数字', 'danger');
                return;
            }

            // 库存数量验证
            const totalCopies = parseInt(form.querySelector('#total_copies').value);
            if (totalCopies < 1) {
                e.preventDefault();
                showAlert('库存数量必须大于0', 'danger');
                return;
            }

            // 必填字段验证
            const requiredFields = ['title', 'author', 'category'];
            for (const field of requiredFields) {
                const input = form.querySelector(`#${field}`);
                if (!input.value.trim()) {
                    e.preventDefault();
                    showAlert(`${input.previousElementSibling.textContent}不能为空`, 'danger');
                    return;
                }
            }
        });

        // ISBN实时验证
        const isbnInput = form.querySelector('#isbn');
        isbnInput.addEventListener('input', function() {
            const isbnRegex = /^(?:\d{10}|\d{13})$/;
            if (this.value && !isbnRegex.test(this.value)) {
                this.classList.add('is-invalid');
                if (!this.nextElementSibling?.classList.contains('invalid-feedback')) {
                    const feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    feedback.textContent = 'ISBN必须是10位或13位数字';
                    this.parentNode.appendChild(feedback);
                }
            } else {
                this.classList.remove('is-invalid');
                this.nextElementSibling?.remove();
            }
        });

        // 数量输入验证
        const copiesInput = form.querySelector('#total_copies');
        copiesInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (value < 1) {
                this.classList.add('is-invalid');
                if (!this.nextElementSibling?.classList.contains('invalid-feedback')) {
                    const feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    feedback.textContent = '库存数量必须大于0';
                    this.parentNode.appendChild(feedback);
                }
            } else {
                this.classList.remove('is-invalid');
                this.nextElementSibling?.remove();
            }
        });
    }
}

// 初始化所有功能
document.addEventListener('DOMContentLoaded', function() {
    // 已有的初始化代码...
    
    // 添加图书表单验证
    validateBookForm();
    
    // 初始化工具提示
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 初始化弹出框
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// 添加图书预览功能
function previewBook() {
    const form = document.querySelector('form[action*="book/add"]');
    if (form) {
        const previewBtn = document.createElement('button');
        previewBtn.type = 'button';
        previewBtn.className = 'btn btn-secondary me-2';
        previewBtn.textContent = '预览';
        previewBtn.onclick = function() {
            const title = form.querySelector('#title').value;
            const author = form.querySelector('#author').value;
            const isbn = form.querySelector('#isbn').value;
            const publisher = form.querySelector('#publisher').value;
            const category = form.querySelector('#category').value;
            const copies = form.querySelector('#total_copies').value;

            const previewHtml = `
                <div class="modal fade" id="previewModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">图书预览</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <h4>${title}</h4>
                                <p><strong>作者：</strong>${author}</p>
                                <p><strong>ISBN：</strong>${isbn}</p>
                                <p><strong>出版社：</strong>${publisher}</p>
                                <p><strong>类别：</strong>${category}</p>
                                <p><strong>库存：</strong>${copies}</p>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // 移除已存在的预览模态框
            document.querySelector('#previewModal')?.remove();
            
            // 添加新的预览模态框
            document.body.insertAdjacentHTML('beforeend', previewHtml);
            
            // 显示预览
            const previewModal = new bootstrap.Modal(document.querySelector('#previewModal'));
            previewModal.show();
        };

        // 添加预览按钮到表单
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.parentNode.insertBefore(previewBtn, submitBtn);
    }
}

// 在页面加载完成后初始化所有功能
document.addEventListener('DOMContentLoaded', function() {
    validateBookForm();
    previewBook();
    initRatingSystem();
    // ... 其他初始化代码 ...
}); 