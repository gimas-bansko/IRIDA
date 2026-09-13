const App = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            edit_mode: false,
            user: {},
            config: {
                school_day_start: '08:00',
                school_lessons_count: 7,
                lesson_duration_minutes: 45,
                first_break_duration_minutes: 20,
                regular_break_duration_minutes: 10,
            },
            editConfig: {},
        };
    },
    methods: {
        sendLogRecord(txt) {
            axios({
                method: 'POST',
                url: '/api/SaveLogRecord/',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                data: {
                    action: txt,
                }
            }).catch(function(error) {
                console.log('Log record error', error);
            });
        },
        loadUserDetails() {
            const vm = this;
            axios.get('/api/context/')
                .then(function(response) {
                    vm.user = response.data;
                });
        },
        loadConfig() {
            const vm = this;
            axios.get('/api/school-day-config/')
                .then(function(response) {
                    if (response.data) {
                        vm.config = response.data;
                    }
                })
                .catch(function(error) {
                    console.error('Error loading school day config:', error);
                });
        },
        startEdit() {
            this.editConfig = JSON.parse(JSON.stringify(this.config));
            this.edit_mode = true;
        },
        cancelEdit() {
            this.edit_mode = false;
        },
        saveConfig() {
            const vm = this;
            axios({
                method: 'PUT',
                url: '/api/school-day-config/',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                data: vm.editConfig
            })
                .then(function(response) {
                    vm.config = response.data;
                    vm.edit_mode = false;
                    vm.sendLogRecord('Редактирани параметри на учебния ден');
                })
                .catch(function(error) {
                    console.error('Error updating school day config:', error);
                });
        }
    },
    created() {
        this.edit_mode = false;
        this.loadUserDetails();
        this.loadConfig();
    }
};

Vue.createApp(App).mount('#main_app');
