const App = {
    delimiters: ['[[', ']]'],
    data() {
        return {
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
            listOfSpecialties:[],
            listOfSubjects:[],
            speciality: {
                "id": 3,
                "specialty_name": "Системно програмиране",
                },
            subject: {
                "id": 1,
                "name": "Интернет програмиране",
                "grade": 12,
                "subject_type": 'теория'
                },
            edit_mode: 'none'
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
                    vm.loadSpecialties()
                    vm.loadSubjects()
                })
        },
        loadSpecialties() {
            // чета списъка на всички специалности които са от същото училище, като влезлия потребител
            const vm = this;
            axios.get('/api/schools/' + vm.user.profile.school.id + '/specialties/')
                .then(function (response) {
                    vm.listOfSpecialties = response.data
                    console.log(vm.listOfSpecialties)
                })
        },
        loadSubjects() {
            // чета списъка на всички предмети, които са от текущо избраната специалност за влезлия потребител
            const vm = this;
            axios.get('/api/specialty/' + vm.user.profile.speciality.id + '/subjects/')
                .then(function (response) {
                    vm.listOfSubjects = response.data
                })
        },
        editSpecialty() {
            this.speciality.id = this.user.profile.speciality.id
            this.speciality.specialty_name = this.user.profile.speciality.specialty_name
            this.edit_mode = 'speciality'
        },
        setSpecialty() {
            this.edit_mode = 'none'
            axios.get(`/api/speciality_select/${this.speciality.id}/`)
                .then(() => {
                    this.loadUserDetails()
                })
                .catch(err => {
                    console.error('Грешка:', err);
                    alert('Възникна грешка!');
                });
        },
        editSubject(){
            this.subject.id = this.user.profile.subject.id
            this.subject.name = this.user.profile.subject.name
            this.subject.grade = this.user.profile.subject.grade
            this.subject.subject_type = this.user.profile.subject.subject_type
            this.edit_mode = 'subject'
        },
        setSubject() {
            this.edit_mode = 'none'
            axios.get(`/api/subject_select/${this.subject.id}/`)
                .then(() => {
                    this.loadUserDetails()
                })
                .catch(err => {
                    console.error('Грешка:', err);
                    alert('Възникна грешка!');
                });
        },
        editGradeSection() {
            this.edit_mode = 'grade_section'
        },
        setGradeSection() {
            this.edit_mode = 'none'
            const gr = this.user.profile.grade
            const se = this.user.profile.section
            axios({
                method: 'POST',
                url: '/api/grade_section_select/',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                data: {
                    'grade': gr,
                    'section': se,
                }
            })
            .then(() => {
                this.loadUserDetails()
            })
            .catch(err => {
                console.error('Грешка:', err);
                alert('Възникна грешка!');
            });
        },
    },
    created(){
        this.loadUserDetails()
    },
}

Vue.createApp(App).mount('#main_app')
