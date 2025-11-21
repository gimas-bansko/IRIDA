const App = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            moscowMap: {
                M: 'Задължителна тема',
                S: 'Важно, но не критично',
                C: 'Пожелателно',
                W: 'Не влиза, Отпада'
            },
            user:{
                "user_id": 1,
                "user_nick": "superadmin",
                "user_name": "Георги Бориков",
                "user_level_num": 1,
                "user_level_text": "Системен администратор",
                "profile": {
                    "access_level": 1,
                    "session_screen": 1,
                    "school": {
                        "id": 1,
                        "short_name": "ПГЕЕ",
                        "full_name": "Професионална гимназия по елктроника и енергетика",
                        "city": "гр. Банско",
                        "logo": "/media_files/sys_pics/school_logo_None_lZ6TrUT.png"
                    },
                    "speciality": {
                        "id": 3,
                        "specialty_num": "4810201",
                        "specialty_name": "Системно програмиране",
                        "level": 3
                    },
                    "grade": 11,
                    "section": "а",
                    "subject": {
                        "id": 1,
                        "name": "Интернет програмиране",
                        "grade": 12,
                        "subject_type": 'теория'
                    },
                    "session": {
                        "id": 1,
                        "num": 1,
                        "name": "Първо занятие 1",
                        "focus": "някакъв фокус на занятието 2",
                        "goals": "основните цели на занятието 1",
                        "duration": 3,
                        "session_type": "НЗ",
                        "basic_level": true
                    }
                }
            },
            listOfSessions:[],
            session:{},
        }
    },
    computed: {
    },
    methods: {
        loadUserDetails() {
            const vm = this;
            axios.get('/api/context/expanded/')
                .then(function (response) {
                    vm.user = response.data
                    vm.session = response.data.profile.session
                    vm.loadSessions(vm.user)
                })
        },
        loadSessions() {
            const vm = this;
            const subjectName = this.user.profile.subject.name;
            const subjectId = this.user.profile.subject.id;
            axios.get(`/api/subjects/${subjectId}/sessions-with-topics/`)
                .then(res => {
                    vm.listOfSessions = res.data;
                })
                .catch(err => {
                    console.error('loadSessions error', err?.response?.data || err);
                    alert('Грешка при зареждане на занятията');
                });
        },
        sessionTypeClass(st) {
            switch (st) {
                case 'НЗ': return 'bg-info';
                case 'УПР': return 'bg-primary';
                case 'ПК': return 'bg-secondary';
                case 'ОС': return 'bg-warning';
                case 'K': return 'bg-success';
                default:  return 'bg-info';
            }
        },
        sessionType(st) {
            switch (st) {
                case 'НЗ': return 'Нови знания';
                case 'УПР': return 'Упражнение';
                case 'ПК': return 'Проверка и контрол';
                case 'ОС': return 'Обобщаване и систематизиране';
                case 'K': return 'Комбиниран урок';
                default:  return '';
            }
        },
        moscowTextFor(topic) {
            const code = topic?.MoSCoW_cat
            return this.moscowMap[code] || code || ''
        },
    },
    created(){
        this.loadUserDetails()
    },
}

Vue.createApp(App).mount('#main_app')
