const App = {
    delimiters: ['[[', ']]'], // Променяме синтаксиса на [[ ]]
    data() {
        return {
            edit_mode:false,
            listOfSpecialties: [],
            user:{},
            school:{},
            specialty:{
                id:0,
                specialty_num:'123',
                specialty_name:"",
                level:3,
                },
        }
    },
    computed: {
        pictureFileName() {
            if (this.school.logo) {
                // Извличаме името на файла от URL
                return this.school.logo.split('/').pop(); // Взема последната част от пътя
            }
            return null; // Ако няма картинка
        },
    },
    methods: {
        onImageChange(e){
            const file = e.target.files[0]
            this.school.logo = URL.createObjectURL(file)
            let formData = new FormData();
            formData.append('id', this.school.id)
            formData.append('logo', file)
            let url =  'api/SchoolLogo/'
            axios.post(url, formData, {headers: {'X-CSRFToken':CSRF_TOKEN, 'Content-Type': 'multipart/form-data'}})
            txt = 'Променено/качено лого на училище '+this.school.short_name+' - '+this.school.city+')'
            this.sendLogRecord(txt)
        },
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
        save() {
            const vm = this;
            axios({
                method: 'PATCH',  // или 'PUT' ако искате да замените целия обект
                url: `/api/schools/${this.school.id}/update/`,
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                data: vm.school
            })
                .then(function(response) {
                    // Може да покажете съобщение за успех или да направите друго действие
                    console.log('School data updated successfully', response.data);
                    // Опционално - обновете информацията
                    vm.school = response.data;

                    // Записване на действието в лога
                    vm.sendLogRecord(`Редактирано училище ${vm.school.short_name} - ${vm.school.city}`);
                })
                .catch(function(error) {
                    console.error('Error updating school data', error);
                    // Тук можете да добавите обработка на грешки
                });
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
        newSpecialty(){
            this.specialty.id = 0
            this.specialty.specialty_num = ''
            this.specialty.specialty_name = ''
            this.specialty.level = 3
            this.edit_mode = true
        },
        editSpecialty(idx){
            this.specialty.id = this.listOfSpecialties[idx].id
            this.specialty.specialty_num = this.listOfSpecialties[idx].specialty_num
            this.specialty.specialty_name = this.listOfSpecialties[idx].specialty_name
            this.specialty.level = this.listOfSpecialties[idx].level
            this.edit_mode = true
        },
        saveSpecialty() {
            vm = this
            vm.edit_mode = false

            // Изпращане на PUT заявка към API
            console.log('/api/specialty/'+vm.specialty.id+'/')
            console.log(vm.specialty.id)
            //axios.put('/api/specialty/'+this.specialty.id+'/', this.specialty, {
            axios.put('api/schools/'+vm.user.user_id+'/specialty/'+vm.specialty.id+'/', vm.specialty, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
                .then(function(response) {
                    vm.loadSpecialties(vm.user)
                    // Показване на съобщение за успех
                    alert("Данните са записани успешно!");
                })
                .catch(function(error) {
                    console.error("Грешка при запазване на данни:", error);
                    alert("Възникна грешка при запазване на данните!");
                });
        },
        setSpecialty(sp_id) {
            axios.get(`/api/speciality_select/${sp_id}/`)
            .then(() => {
              window.location.href = '/subjects';
            })
            .catch(err => {
              console.error('Грешка:', err);
              alert('Възникна грешка!');
            });
        },
    },
    created: function(){
        this.status = 0
        this.loadUserDetails();
    }
}

Vue.createApp(App).mount('#main_app')
