const App = {
    delimiters: ['[[', ']]'],
    data() {
        return {
            user:{},
            listOfSpecialties:[],
            listOfSubjects:[],
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
                    console.log(vm.user);
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
                    console.log(vm.listOfSubjects)
                })
        },
    },
    created(){
        this.loadUserDetails()
    },
}

Vue.createApp(App).mount('#main_app')