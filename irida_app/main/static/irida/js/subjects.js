const App = {
    delimiters: ['[[', ']]'], // Променяме синтаксиса на [[ ]]
    data() {
        return {
            edit_mode:0, // 0 - списък; 1 - едактиране на предмет
            listOfSpecialties: [],
            listOfSubjects: [],
            user:{},
            school:{},
            subject:{
                id:0,
                name: '',
                grade: 12,
                subject_type: true,
                hpy: 18,
                wpy: 0,
                hpw1: 0,
                hpw2: 0,
                },
        }
    },
    computed: {

    },
    methods: {
        sendLogRecord(txt){
            const vm=this
            axios({
                method:'POST',
                url:'/api/SaveLogRecord/',
                headers:{
                    'X-CSRFToken':CSRF_TOKEN,
                    //'Access-Control-Allow-Origin':'*',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                data:{
                    action: txt,
                }
            })
        },
        loadSchool(logged_user){
            // чета всички данни за училището на влезлия потребител
            const vm = this;
            axios.get('/api/schools/'+logged_user.school+'/')
                .then(function(response){
                    vm.school = response.data
                })
        },
        loadUserDetails(){
            const vm = this;
            axios.get('/api/context/')
                .then(function(response){
                    vm.user = response.data
                    vm.loadSpecialties(vm.user)
                    vm.loadSchool(vm.user)
                    vm.loadSubjects(vm.user)
                })
        },
        loadSpecialties(logged_user){
            // чета списъка на всички специалности които са от същото училище, като влезлия потребител
            const vm = this;
            axios.get('/api/schools/'+logged_user.school+'/specialties/')
                .then(function(response){
                    vm.listOfSpecialties = response.data
                })
        },
        loadSubjects(logged_user){
            // чета списъка на всички предмети, които са от текущо избраната специалност за влезлия потребител
            const vm = this;
            axios.get('/api/specialty/'+logged_user.specialty+'/subjects/')
                .then(function(response){
                    vm.listOfSubjects = response.data
                    console.log(vm.listOfSubjects)
                })
        },
        newSubject(){
            this.subject.id = 0,
            this.subject.name = '',
            this.subject.grade = 12,
            this.subject.subject_type = true,
            this.subject.hpy = 18,
            this.subject.wpy = 0,
            this.subject.hpw1 = 0,
            this.subject.hpw2 = 0,
            this.edit_mode = 1
        },
        editSubject(idx){
            this.subject.id = this.listOfSubjects[idx].id
            this.subject.name = this.listOfSubjects[idx].name
            this.subject.grade = this.listOfSubjects[idx].grade
            this.subject.subject_type = this.listOfSubjects[idx].subject_type
            this.subject.hpy = this.listOfSubjects[idx].hpy
            this.subject.wpy = this.listOfSubjects[idx].wpy
            this.subject.hpw1 = this.listOfSubjects[idx].hpw1
            this.subject.hpw2 = this.listOfSubjects[idx].hpw2
            this.edit_mode = 1
        },
        saveSubject() {
            vm = this
            vm.edit_mode = 0

            // Изпращане на PUT заявка към API
            axios.put('api/specialty/'+vm.user.specialty+'/subjects/'+vm.subject.id+'/', vm.subject, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
                .then(function(response) {
                    vm.loadSubjects(vm.user)
                    // Показване на съобщение за успех
                    alert("Данните са записани успешно!");
                })
                .catch(function(error) {
                    console.error("Грешка при запазване на данни:", error);
                    alert("Възникна грешка при запазване на данните!");
                });
        },
        subjectTypeStr(idx) {
            if (this.listOfSubjects[idx].subject_type) {
                return 'теория'
            }
            return 'практика'
        },
    },
    created: function(){
        console.log('subject.js')
        this.status = 0
        this.loadUserDetails();
    }
}

Vue.createApp(App).mount('#main_app')
