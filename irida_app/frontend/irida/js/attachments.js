/**
 * IRIDA - Управление на глобални приложения и файлове
 */

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const CSRF_TOKEN = window.CSRF_TOKEN || getCookie('csrftoken') || '';

const App = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            attachments: [],
            filterType: 'all', // 'all', 'system', 'mine'
            attachmentEditMode: false,
            selectedAttachmentFile: null,
            isMarkdownFileSelected: false,
            originalFileName: '',
            attachmentForm: {
                id: 0,
                num: 1,
                name: '',
                file_url: null,
                file_name: '',
                original_filename: '',
                description: '',
                is_system: false,
                target_format: 'docx',
            },
        };
    },
    computed: {
        filteredAttachments() {
            if (this.filterType === 'system') {
                return this.attachments.filter(a => !!a.is_system);
            }
            if (this.filterType === 'mine') {
                return this.attachments.filter(a => this.isOwner(a));
            }
            return this.attachments;
        },
        countSystem() {
            return this.attachments.filter(a => !!a.is_system).length;
        },
        countMine() {
            return this.attachments.filter(a => this.isOwner(a)).length;
        },
    },
    methods: {
        setFilter(type) {
            this.filterType = type;
        },
        isOwner(a) {
            if (!a) return false;
            if (a.is_owner === true) return true;
            if (window.CURRENT_USER_ID && a.created_by && Number(a.created_by) === Number(window.CURRENT_USER_ID)) {
                return true;
            }
            return false;
        },
        loadAttachments() {
            const vm = this;
            axios.get('/api/app-attachments/')
                .then(function(response) {
                    if (response.data) {
                        vm.attachments = response.data;
                    }
                })
                .catch(function(error) {
                    console.error('Грешка при зареждане на приложения:', error);
                });
        },
        startCreateAttachment() {
            const nextNum = this.attachments.length
                ? Math.max(...this.attachments.map(a => a.num || 0)) + 1
                : 1;

            this.attachmentForm = {
                id: 0,
                num: nextNum,
                name: '',
                file_url: null,
                file_name: '',
                original_filename: '',
                description: '',
                is_system: false,
                target_format: 'docx',
            };
            this.selectedAttachmentFile = null;
            this.isMarkdownFileSelected = false;
            this.originalFileName = '';

            const fileInput = document.getElementById('appAttachmentFileInput');
            if (fileInput) fileInput.value = '';

            this.attachmentEditMode = true;
        },
        startEditAttachment(a) {
            this.attachmentForm = {
                id: a.id,
                num: a.num,
                name: a.name,
                file_url: a.file_url,
                file_name: a.file_name,
                original_filename: a.original_filename || a.file_name || '',
                description: a.description || '',
                is_system: !!a.is_system,
                target_format: 'docx',
            };
            this.selectedAttachmentFile = null;
            this.isMarkdownFileSelected = false;
            this.originalFileName = '';

            const fileInput = document.getElementById('appAttachmentFileInput');
            if (fileInput) fileInput.value = '';

            this.attachmentEditMode = true;
        },
        onAttachmentFileChange(e) {
            const file = e.target.files && e.target.files[0];
            this.selectedAttachmentFile = file || null;

            if (file) {
                const fname = file.name.toLowerCase();
                const isMd = fname.endsWith('.md') || fname.endsWith('.markdown');
                this.isMarkdownFileSelected = isMd;
                this.originalFileName = file.name;

                if (isMd) {
                    this.attachmentForm.target_format = 'docx';
                    if (!this.attachmentForm.name || this.attachmentForm.name === this.attachmentForm.file_name || this.attachmentForm.name === this.attachmentForm.original_filename) {
                        const baseName = file.name.replace(/\.(md|markdown)$/i, '');
                        this.attachmentForm.name = baseName + '.docx';
                    }
                } else {
                    this.attachmentForm.target_format = 'original';
                    if (!this.attachmentForm.name || this.attachmentForm.name === this.attachmentForm.file_name || this.attachmentForm.name === this.attachmentForm.original_filename) {
                        this.attachmentForm.name = file.name;
                    }
                }
            } else {
                this.isMarkdownFileSelected = false;
                this.selectedAttachmentFile = null;
                this.originalFileName = '';
            }
        },
        onTargetFormatChange() {
            if (!this.isMarkdownFileSelected || !this.originalFileName) return;

            const baseName = this.originalFileName.replace(/\.(md|markdown)$/i, '');
            const currentName = (this.attachmentForm.name || '').trim();

            if (
                !currentName ||
                currentName === this.originalFileName ||
                currentName === baseName + '.docx' ||
                currentName === baseName + '.pdf' ||
                currentName === baseName + '.md'
            ) {
                if (this.attachmentForm.target_format === 'docx') {
                    this.attachmentForm.name = baseName + '.docx';
                } else if (this.attachmentForm.target_format === 'pdf') {
                    this.attachmentForm.name = baseName + '.pdf';
                } else {
                    this.attachmentForm.name = this.originalFileName;
                }
            }
        },
        cancelAttachmentEdit() {
            this.attachmentEditMode = false;
            this.selectedAttachmentFile = null;
            this.isMarkdownFileSelected = false;
            this.originalFileName = '';
            const fileInput = document.getElementById('appAttachmentFileInput');
            if (fileInput) fileInput.value = '';
        },
        saveAttachment() {
            const vm = this;
            const nameVal = (vm.attachmentForm.name || '').trim();
            if (!nameVal) {
                alert('Моля, въведете име / заглавие на приложението.');
                return;
            }
            if (!vm.attachmentForm.id && !vm.selectedAttachmentFile) {
                alert('Моля, изберете файл за прикачване.');
                return;
            }

            const formData = new FormData();
            formData.append('id', vm.attachmentForm.id || 0);
            formData.append('num', vm.attachmentForm.num || 1);
            formData.append('name', nameVal);
            formData.append('description', vm.attachmentForm.description || '');
            formData.append('is_system', vm.attachmentForm.is_system ? 'true' : 'false');

            if (vm.selectedAttachmentFile) {
                formData.append('file', vm.selectedAttachmentFile);
                if (vm.isMarkdownFileSelected) {
                    formData.append('target_format', vm.attachmentForm.target_format || 'original');
                }
            }

            axios({
                method: 'POST',
                url: '/api/app-attachments/upsert/',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                },
                data: formData,
            })
                .then(function(response) {
                    vm.attachmentEditMode = false;
                    vm.selectedAttachmentFile = null;
                    vm.isMarkdownFileSelected = false;
                    vm.originalFileName = '';
                    vm.loadAttachments();
                })
                .catch(function(error) {
                    console.error('Грешка при запис на приложение:', error);
                    let errorDetail = error.response?.data?.detail || error.response?.data?.error;
                    if (!errorDetail && error.response?.data && typeof error.response.data === 'object') {
                        const errors = Object.values(error.response.data).flat();
                        if (errors.length > 0) {
                            errorDetail = errors.join('; ');
                        }
                    }
                    if (!errorDetail) {
                        errorDetail = 'Възникна грешка при записа на приложението.';
                    }
                    alert(errorDetail);
                });
        },
        deleteAttachment(a) {
            const vm = this;
            axios({
                method: 'DELETE',
                url: `/api/app-attachments/${a.id}/`,
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                },
            })
                .then(function(response) {
                    vm.loadAttachments();
                })
                .catch(function(error) {
                    console.error('Грешка при изтриване на приложение:', error);
                    alert('Възникна грешка при изтриването на приложението.');
                });
        },
        downloadFile(fileUrl, fileName) {
            if (!fileUrl) return;
            axios.get(fileUrl, { responseType: 'blob' })
                .then(function(response) {
                    const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = blobUrl;
                    link.setAttribute('download', fileName || 'attachment');
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                    window.URL.revokeObjectURL(blobUrl);
                })
                .catch(function(error) {
                    console.error('Грешка при сваляне на файла:', error);
                    const link = document.createElement('a');
                    link.href = fileUrl;
                    link.setAttribute('download', fileName || '');
                    link.target = '_blank';
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                });
        },
    },
    created() {
        this.loadAttachments();
    },
};

Vue.createApp(App).mount('#main_app');
