<<<<<<< HEAD
// Utility functions
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.main-content') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showLoading(button) {
    const originalText = button.textContent;
    button.innerHTML = '<span class="loading"></span> Đang xử lý...';
    button.disabled = true;
    return originalText;
}

function hideLoading(button, originalText) {
    button.textContent = originalText;
    button.disabled = false;
}

// Modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // If this is an assignment modal, load technicians
        if (modalId.startsWith('assignModal')) {
            const ticketId = modalId.replace('assignModal', '');
            loadTechnicians(ticketId);
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
}

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            field.style.borderColor = '#e1e5e9';
        }
    });
    
    return isValid;
}

// Ticket assignment
async function assignTicket(ticketId) {
    const technicianSelect = document.getElementById(`technician-${ticketId}`);
    const technicianId = technicianSelect.value;
    
    if (!technicianId) {
        showAlert('Vui lòng chọn kỹ thuật viên!', 'loi');
        return;
    }
    
    const formData = new FormData();
    formData.append('technician_id', technicianId);
    
    try {
        const response = await fetch(`/tickets/${ticketId}/assign`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showAlert('Điều phiếu thành công!', 'thanh_cong');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('Có lỗi xảy ra khi điều phiếu!', 'loi');
        }
    } catch (error) {
        showAlert('Có lỗi xảy ra khi kết nối server!', 'loi');
    }
}

// Load technicians for assignment modal
async function loadTechnicians(ticketId) {
    try {
        const response = await fetch('/api/technicians');
        const technicians = await response.json();
        
        const select = document.getElementById(`technician-${ticketId}`);
        const noTechniciansDiv = document.getElementById(`no-technicians-${ticketId}`);
        const assignBtn = document.getElementById(`assign-btn-${ticketId}`);
        
        // Clear existing options
        select.innerHTML = '<option value="">Chọn kỹ thuật viên...</option>';
        
        if (technicians.length === 0) {
            // No technicians online
            noTechniciansDiv.style.display = 'block';
            assignBtn.disabled = true;
            assignBtn.textContent = 'Không thể điều phiếu';
        } else {
            // Add technician options
            technicians.forEach(tech => {
                const option = document.createElement('option');
                option.value = tech.id;
                option.textContent = tech.username;
                select.appendChild(option);
            });
            
            noTechniciansDiv.style.display = 'none';
            assignBtn.disabled = false;
            assignBtn.textContent = 'Điều phiếu';
        }
    } catch (error) {
        console.error('Error loading technicians:', error);
        showAlert('Có lỗi xảy ra khi tải danh sách kỹ thuật viên!', 'loi');
    }
}

// Accept ticket
async function acceptTicket(ticketId) {
    if (!confirm('Bạn có chắc muốn nhận phiếu này?')) {
        return;
    }
    
    try {
        const response = await fetch(`/tickets/${ticketId}/accept`, {
            method: 'POST'
        });
        
        if (response.ok) {
            showAlert('Đã nhận phiếu thành công!', 'thanh_cong');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('Có lỗi xảy ra khi nhận phiếu!', 'loi');
        }
    } catch (error) {
        showAlert('Có lỗi xảy ra khi kết nối server!', 'loi');
    }
}

// Complete ticket
async function completeTicket(ticketId) {
    const notes = document.getElementById(`completion-notes-${ticketId}`).value;
    
    const formData = new FormData();
    formData.append('completion_notes', notes);
    
    try {
        const response = await fetch(`/tickets/${ticketId}/complete`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showAlert('Hoàn thành phiếu thành công!', 'thanh_cong');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('Có lỗi xảy ra khi hoàn thành phiếu!', 'loi');
        }
    } catch (error) {
        showAlert('Có lỗi xảy ra khi kết nối server!', 'loi');
    }
}

// Delete ticket
async function deleteTicket(ticketId) {
    if (!confirm('Bạn có chắc muốn xóa phiếu này? Hành động này không thể hoàn tác!')) {
        return;
    }
    
    try {
        const response = await fetch(`/tickets/${ticketId}/delete`, {
            method: 'POST'
        });
        
        if (response.ok) {
            showAlert('Đã xóa phiếu thành công!', 'thanh_cong');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('Có lỗi xảy ra khi xóa phiếu!', 'loi');
        }
    } catch (error) {
        showAlert('Có lỗi xảy ra khi kết nối server!', 'loi');
    }
}

// Update ticket status
async function updateTicketStatus(ticketId) {
    const statusSelect = document.getElementById(`status-${ticketId}`);
    const notesTextarea = document.getElementById(`notes-${ticketId}`);
    
    const status = statusSelect.value;
    const notes = notesTextarea ? notesTextarea.value : '';
    
    if (!status) {
        showAlert('Vui lòng chọn trạng thái!', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('status', status);
    formData.append('completion_notes', notes);
    
    try {
        const response = await fetch(`/tickets/${ticketId}/update_status`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showAlert('Cập nhật trạng thái thành công!', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('Có lỗi xảy ra khi cập nhật trạng thái!', 'error');
        }
    } catch (error) {
        showAlert('Có lỗi xảy ra khi kết nối server!', 'error');
    }
}

// Load technicians for assignment
async function loadTechnicians() {
    try {
        const response = await fetch('/api/technicians');
        if (response.ok) {
            const technicians = await response.json();
            const selects = document.querySelectorAll('[id^="technician-"]');
            
            selects.forEach(select => {
                select.innerHTML = '<option value="">Chọn kỹ thuật viên...</option>';
                technicians.forEach(tech => {
                    const option = document.createElement('option');
                    option.value = tech.id;
                    option.textContent = tech.username;
                    select.appendChild(option);
                });
            });
        }
    } catch (error) {
        console.error('Error loading technicians:', error);
    }
}

// Search and filter functionality
function filterTickets() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const statusFilter = document.getElementById('status-filter').value;
    const priorityFilter = document.getElementById('priority-filter').value;
    
    const tickets = document.querySelectorAll('.ticket-card');
    
    tickets.forEach(ticket => {
        const ticketNumber = ticket.querySelector('.ticket-number').textContent.toLowerCase();
        const customerName = ticket.querySelector('.ticket-info h3').textContent.toLowerCase();
        const status = ticket.querySelector('.ticket-status').textContent.toLowerCase();
        const priority = ticket.querySelector('.ticket-priority').textContent.toLowerCase();
        
        let showTicket = true;
        
        // Search filter
        if (searchTerm && !ticketNumber.includes(searchTerm) && !customerName.includes(searchTerm)) {
            showTicket = false;
        }
        
        // Status filter
        if (statusFilter && status !== statusFilter.toLowerCase()) {
            showTicket = false;
        }
        
        // Priority filter
        if (priorityFilter && priority !== priorityFilter.toLowerCase()) {
            showTicket = false;
        }
        
        ticket.style.display = showTicket ? 'block' : 'none';
    });
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Load technicians if on dashboard
    if (document.querySelector('[id^="technician-"]')) {
        loadTechnicians();
    }
    
    // Initialize search and filter functionality
    initializeSearchAndFilter();
    
    // Setup search and filter
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const priorityFilter = document.getElementById('priority-filter');
    
    if (searchInput) {
        searchInput.addEventListener('input', filterTickets);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterTickets);
    }
    
    if (priorityFilter) {
        priorityFilter.addEventListener('change', filterTickets);
    }
    
    // Setup form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showAlert('Vui lòng điền đầy đủ thông tin bắt buộc!', 'error');
            }
        });
    });
    
    // Setup close buttons for modals
    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.remove();
        }, 5000);
    });
});

// Mobile menu toggle
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

// Responsive table
function makeTableResponsive() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-responsive';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });
}

// Initialize responsive table
document.addEventListener('DOMContentLoaded', makeTableResponsive);

// Export functionality
// Search and filter functionality
function initializeSearchAndFilter() {
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const priorityFilter = document.getElementById('priority-filter');
    
    if (searchInput) {
        searchInput.addEventListener('input', debounce(applyFilters, 300));
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', applyFilters);
    }
    
    if (priorityFilter) {
        priorityFilter.addEventListener('change', applyFilters);
    }
}

function applyFilters() {
    const searchTerm = document.getElementById('search-input')?.value || '';
    const statusFilter = document.getElementById('status-filter')?.value || '';
    const priorityFilter = document.getElementById('priority-filter')?.value || '';
    
    // Build query string
    const params = new URLSearchParams();
    if (searchTerm) params.append('search', searchTerm);
    if (statusFilter) params.append('status', statusFilter);
    if (priorityFilter) params.append('priority', priorityFilter);
    
    // Redirect to search route
    window.location.href = `/tickets/search?${params.toString()}`;
}

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function exportTickets() {
    const tickets = document.querySelectorAll('.ticket-card');
    let csvContent = 'data:text/csv;charset=utf-8,';
    csvContent += 'Số phiếu,Tên khách hàng,Địa chỉ,Số điện thoại,Mô tả,Độ ưu tiên,Trạng thái,Ngày tạo,Ngày phân công,Ngày nhận,Ngày hoàn thành\n';
    
    tickets.forEach(ticket => {
        const ticketNumber = ticket.querySelector('.ticket-number').textContent;
        const customerName = ticket.querySelector('.ticket-info h3').textContent;
        const customerAddress = ticket.querySelector('.ticket-info p:nth-child(2)').textContent.replace('Địa chỉ: ', '');
        const customerPhone = ticket.querySelector('.ticket-info p:nth-child(3)').textContent.replace('Mô tả: ', '');
        const description = ticket.querySelector('.ticket-info p:nth-child(4)').textContent.replace('Mô tả: ', '');
        const priority = ticket.querySelector('.ticket-priority').textContent;
        const status = ticket.querySelector('.ticket-status').textContent;
        const createdAt = ticket.querySelector('.ticket-info p:nth-child(5)').textContent.replace('Ngày tạo: ', '');
        
        // Get additional dates if available
        const assignedDate = ticket.querySelector('p:nth-child(6)')?.textContent.replace('Ngày phân công: ', '') || '';
        const acceptedDate = ticket.querySelector('p:nth-child(7)')?.textContent.replace('Ngày nhận: ', '') || '';
        const completedDate = ticket.querySelector('p:nth-child(8)')?.textContent.replace('Ngày hoàn thành: ', '') || '';
        
        csvContent += `"${ticketNumber}","${customerName}","${customerAddress}","${customerPhone}","${description}","${priority}","${status}","${createdAt}","${assignedDate}","${acceptedDate}","${completedDate}"\n`;
    });
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `tickets_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Cập nhật trạng thái online/offline của user
function updateUserStatus(isOnline) {
    fetch('/api/update_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ is_online: isOnline })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Cập nhật trạng thái thành công');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Cập nhật trạng thái khi user rời trang
window.addEventListener('beforeunload', function() {
    updateUserStatus(false);
});

// Cập nhật trạng thái khi user vào trang và định kỳ
document.addEventListener('DOMContentLoaded', function() {
    // Cập nhật trạng thái online khi vào trang
    updateUserStatus(true);
    
    // Cập nhật trạng thái mỗi 30 giây
    setInterval(() => {
        updateUserStatus(true);
    }, 30000);
    
    // Khởi tạo search và filter
    initializeSearchAndFilter();
});
=======
// Utility functions
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.main-content') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showLoading(button) {
    const originalText = button.textContent;
    button.innerHTML = '<span class="loading"></span> Đang xử lý...';
    button.disabled = true;
    return originalText;
}

function hideLoading(button, originalText) {
    button.textContent = originalText;
    button.disabled = false;
}

// Modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // If this is an assignment modal, load technicians
        if (modalId.startsWith('assignModal')) {
            const ticketId = modalId.replace('assignModal', '');
            loadTechnicians(ticketId);
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
}

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            field.style.borderColor = '#e1e5e9';
        }
    });
    
    return isValid;
}

// Ticket assignment
async function assignTicket(ticketId) {
    const technicianSelect = document.getElementById(`technician-${ticketId}`);
    const technicianId = technicianSelect.value;
    
    if (!technicianId) {
        showAlert('Vui lòng chọn kỹ thuật viên!', 'loi');
        return;
    }
    
    const formData = new FormData();
    formData.append('technician_id', technicianId);
    
    try {
        const response = await fetch(`/tickets/${ticketId}/assign`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showAlert('Điều phiếu thành công!', 'thanh_cong');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('Có lỗi xảy ra khi điều phiếu!', 'loi');
        }
    } catch (error) {
        showAlert('Có lỗi xảy ra khi kết nối server!', 'loi');
    }
}

// Load technicians for assignment modal
async function loadTechnicians(ticketId) {
    try {
        const response = await fetch('/api/technicians');
        const technicians = await response.json();
        
        const select = document.getElementById(`technician-${ticketId}`);
        const noTechniciansDiv = document.getElementById(`no-technicians-${ticketId}`);
        const assignBtn = document.getElementById(`assign-btn-${ticketId}`);
        
        // Clear existing options
        select.innerHTML = '<option value="">Chọn kỹ thuật viên...</option>';
        
        if (technicians.length === 0) {
            // No technicians online
            noTechniciansDiv.style.display = 'block';
            assignBtn.disabled = true;
            assignBtn.textContent = 'Không thể điều phiếu';
        } else {
            // Add technician options
            technicians.forEach(tech => {
                const option = document.createElement('option');
                option.value = tech.id;
                option.textContent = tech.username;
                select.appendChild(option);
            });
            
            noTechniciansDiv.style.display = 'none';
            assignBtn.disabled = false;
            assignBtn.textContent = 'Điều phiếu';
        }
    } catch (error) {
        console.error('Error loading technicians:', error);
        showAlert('Có lỗi xảy ra khi tải danh sách kỹ thuật viên!', 'loi');
    }
}

// Accept ticket
async function acceptTicket(ticketId) {
    if (!confirm('Bạn có chắc muốn nhận phiếu này?')) {
        return;
    }
    
    try {
        const response = await fetch(`/tickets/${ticketId}/accept`, {
            method: 'POST'
        });
        
        if (response.ok) {
            showAlert('Đã nhận phiếu thành công!', 'thanh_cong');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('Có lỗi xảy ra khi nhận phiếu!', 'loi');
        }
    } catch (error) {
        showAlert('Có lỗi xảy ra khi kết nối server!', 'loi');
    }
}

// Complete ticket
async function completeTicket(ticketId) {
    const notes = document.getElementById(`completion-notes-${ticketId}`).value;
    
    const formData = new FormData();
    formData.append('completion_notes', notes);
    
    try {
        const response = await fetch(`/tickets/${ticketId}/complete`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showAlert('Hoàn thành phiếu thành công!', 'thanh_cong');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('Có lỗi xảy ra khi hoàn thành phiếu!', 'loi');
        }
    } catch (error) {
        showAlert('Có lỗi xảy ra khi kết nối server!', 'loi');
    }
}

// Delete ticket
async function deleteTicket(ticketId) {
    if (!confirm('Bạn có chắc muốn xóa phiếu này? Hành động này không thể hoàn tác!')) {
        return;
    }
    
    try {
        const response = await fetch(`/tickets/${ticketId}/delete`, {
            method: 'POST'
        });
        
        if (response.ok) {
            showAlert('Đã xóa phiếu thành công!', 'thanh_cong');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('Có lỗi xảy ra khi xóa phiếu!', 'loi');
        }
    } catch (error) {
        showAlert('Có lỗi xảy ra khi kết nối server!', 'loi');
    }
}

// Update ticket status
async function updateTicketStatus(ticketId) {
    const statusSelect = document.getElementById(`status-${ticketId}`);
    const notesTextarea = document.getElementById(`notes-${ticketId}`);
    
    const status = statusSelect.value;
    const notes = notesTextarea ? notesTextarea.value : '';
    
    if (!status) {
        showAlert('Vui lòng chọn trạng thái!', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('status', status);
    formData.append('completion_notes', notes);
    
    try {
        const response = await fetch(`/tickets/${ticketId}/update_status`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showAlert('Cập nhật trạng thái thành công!', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('Có lỗi xảy ra khi cập nhật trạng thái!', 'error');
        }
    } catch (error) {
        showAlert('Có lỗi xảy ra khi kết nối server!', 'error');
    }
}

// Load technicians for assignment
async function loadTechnicians() {
    try {
        const response = await fetch('/api/technicians');
        if (response.ok) {
            const technicians = await response.json();
            const selects = document.querySelectorAll('[id^="technician-"]');
            
            selects.forEach(select => {
                select.innerHTML = '<option value="">Chọn kỹ thuật viên...</option>';
                technicians.forEach(tech => {
                    const option = document.createElement('option');
                    option.value = tech.id;
                    option.textContent = tech.username;
                    select.appendChild(option);
                });
            });
        }
    } catch (error) {
        console.error('Error loading technicians:', error);
    }
}

// Search and filter functionality
function filterTickets() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const statusFilter = document.getElementById('status-filter').value;
    const priorityFilter = document.getElementById('priority-filter').value;
    
    const tickets = document.querySelectorAll('.ticket-card');
    
    tickets.forEach(ticket => {
        const ticketNumber = ticket.querySelector('.ticket-number').textContent.toLowerCase();
        const customerName = ticket.querySelector('.ticket-info h3').textContent.toLowerCase();
        const status = ticket.querySelector('.ticket-status').textContent.toLowerCase();
        const priority = ticket.querySelector('.ticket-priority').textContent.toLowerCase();
        
        let showTicket = true;
        
        // Search filter
        if (searchTerm && !ticketNumber.includes(searchTerm) && !customerName.includes(searchTerm)) {
            showTicket = false;
        }
        
        // Status filter
        if (statusFilter && status !== statusFilter.toLowerCase()) {
            showTicket = false;
        }
        
        // Priority filter
        if (priorityFilter && priority !== priorityFilter.toLowerCase()) {
            showTicket = false;
        }
        
        ticket.style.display = showTicket ? 'block' : 'none';
    });
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Load technicians if on dashboard
    if (document.querySelector('[id^="technician-"]')) {
        loadTechnicians();
    }
    
    // Initialize search and filter functionality
    initializeSearchAndFilter();
    
    // Setup search and filter
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const priorityFilter = document.getElementById('priority-filter');
    
    if (searchInput) {
        searchInput.addEventListener('input', filterTickets);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterTickets);
    }
    
    if (priorityFilter) {
        priorityFilter.addEventListener('change', filterTickets);
    }
    
    // Setup form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showAlert('Vui lòng điền đầy đủ thông tin bắt buộc!', 'error');
            }
        });
    });
    
    // Setup close buttons for modals
    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.remove();
        }, 5000);
    });
});

// Mobile menu toggle
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

// Responsive table
function makeTableResponsive() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-responsive';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });
}

// Initialize responsive table
document.addEventListener('DOMContentLoaded', makeTableResponsive);

// Export functionality
// Search and filter functionality
function initializeSearchAndFilter() {
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const priorityFilter = document.getElementById('priority-filter');
    
    if (searchInput) {
        searchInput.addEventListener('input', debounce(applyFilters, 300));
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', applyFilters);
    }
    
    if (priorityFilter) {
        priorityFilter.addEventListener('change', applyFilters);
    }
}

function applyFilters() {
    const searchTerm = document.getElementById('search-input')?.value || '';
    const statusFilter = document.getElementById('status-filter')?.value || '';
    const priorityFilter = document.getElementById('priority-filter')?.value || '';
    
    // Build query string
    const params = new URLSearchParams();
    if (searchTerm) params.append('search', searchTerm);
    if (statusFilter) params.append('status', statusFilter);
    if (priorityFilter) params.append('priority', priorityFilter);
    
    // Redirect to search route
    window.location.href = `/tickets/search?${params.toString()}`;
}

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function exportTickets() {
    const tickets = document.querySelectorAll('.ticket-card');
    let csvContent = 'data:text/csv;charset=utf-8,';
    csvContent += 'Số phiếu,Tên khách hàng,Địa chỉ,Số điện thoại,Mô tả,Độ ưu tiên,Trạng thái,Ngày tạo,Ngày phân công,Ngày nhận,Ngày hoàn thành\n';
    
    tickets.forEach(ticket => {
        const ticketNumber = ticket.querySelector('.ticket-number').textContent;
        const customerName = ticket.querySelector('.ticket-info h3').textContent;
        const customerAddress = ticket.querySelector('.ticket-info p:nth-child(2)').textContent.replace('Địa chỉ: ', '');
        const customerPhone = ticket.querySelector('.ticket-info p:nth-child(3)').textContent.replace('Mô tả: ', '');
        const description = ticket.querySelector('.ticket-info p:nth-child(4)').textContent.replace('Mô tả: ', '');
        const priority = ticket.querySelector('.ticket-priority').textContent;
        const status = ticket.querySelector('.ticket-status').textContent;
        const createdAt = ticket.querySelector('.ticket-info p:nth-child(5)').textContent.replace('Ngày tạo: ', '');
        
        // Get additional dates if available
        const assignedDate = ticket.querySelector('p:nth-child(6)')?.textContent.replace('Ngày phân công: ', '') || '';
        const acceptedDate = ticket.querySelector('p:nth-child(7)')?.textContent.replace('Ngày nhận: ', '') || '';
        const completedDate = ticket.querySelector('p:nth-child(8)')?.textContent.replace('Ngày hoàn thành: ', '') || '';
        
        csvContent += `"${ticketNumber}","${customerName}","${customerAddress}","${customerPhone}","${description}","${priority}","${status}","${createdAt}","${assignedDate}","${acceptedDate}","${completedDate}"\n`;
    });
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `tickets_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Cập nhật trạng thái online/offline của user
function updateUserStatus(isOnline) {
    fetch('/api/update_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ is_online: isOnline })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Cập nhật trạng thái thành công');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Cập nhật trạng thái khi user rời trang
window.addEventListener('beforeunload', function() {
    updateUserStatus(false);
});

// Cập nhật trạng thái khi user vào trang và định kỳ
document.addEventListener('DOMContentLoaded', function() {
    // Cập nhật trạng thái online khi vào trang
    updateUserStatus(true);
    
    // Cập nhật trạng thái mỗi 30 giây
    setInterval(() => {
        updateUserStatus(true);
    }, 30000);
    
    // Khởi tạo search và filter
    initializeSearchAndFilter();
});
>>>>>>> cad4acc09904766658dc682f1d2e0e72db707bbf
