const App = {
    delimiters: ['[[', ']]'], // Променяме синтаксиса на [[ ]]
    data() {
        return {
            moscowMap: {
                M: 'Задължителна тема',
                S: 'Важно, но не критично',
                C: 'Пожелателно',
                W: 'Не влиза, Отпада'
            },
            edit:{
                editor:false, //режима на редактиране (да/не)
                index:-1, // -1 - нов; >-1 -индекс
                level:0, // ниво 0 е външно, 1 е вътрешно
            },
            listOfSpecialties: [],
            listOfSubjects: [],
            listOfGoals: [],
            listOfUnits:[],
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
            goal:{
                id:0,
                num:0,
                name:'',
                course:0,
            },
            unit: { id: 0, num: 1, name: '', hours: 1, subject: 0 },
            topic: { id: 0, num: 1, name: '', MoSCoW_cat: 'M', MoSCoW_rem: '', unit: 0 },
            totalHours:0,
        }
    },
    computed: {
        currentTopicMoSCoWText() {
            const code = this.topic?.MoSCoW_cat || 'M'
            return this.moscowMap[code] || code
        },
        totalHours() {
            // защита при липсващ или неинициализиран списък
            if (!Array.isArray(this.listOfUnits)) return 0;

            return this.listOfUnits.reduce((sum, u) => {
                // гарантираме числова стойност, дори ако hours е string или undefined
                const h = Number(u?.hours ?? 0);
                return sum + (isNaN(h) ? 0 : h);
            }, 0);
        }
    },
    methods: {
        moscowTextFor(topic) {
            const code = topic?.MoSCoW_cat
            return this.moscowMap[code] || code || ''
        },

        // методи за показване/скриване на редактора
        setEditMode(lvl,idx){
            this.edit.editor = true
            this.edit.index = idx
            this.edit.level = lvl
        },
        clearEditMode(){
            this.edit.editor = false
        },
        showItem(lvl,idx){
            let result=true
            if(this.edit.editor){
                if((this.edit.index===idx)&&(this.edit.level===lvl)){
                    result=false
                }
            }
            return result
        },
        showEditor(lvl,idx){
            let result=false
            if(this.edit.editor){
                if((this.edit.index===idx)&&(this.edit.level===lvl)){
                    result=true
                }
            }
            return result
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
                    vm.loadGoals(vm.user)
                    vm.loadUnits(vm.user)
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
            this.subject.id = 0
            this.subject.name = ''
            this.subject.grade = 12
            this.subject.subject_type = true
            this.subject.hpy = 18
            this.subject.wpy = 0
            this.subject.hpw1 = 0
            this.subject.hpw2 = 0
            this.clearEditMode()
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
            this.setEditMode(0,idx)
        },
        saveSubject() {
            vm = this
            vm.clearEditMode()

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
        setSubjectGoal(sb_id) {
            axios.get(`/api/course_set/${sb_id}/`)
                .then(() => {
                    window.location.href = '/goals';
                })
                .catch(err => {
                    console.error('Грешка:', err);
                    alert('Възникна грешка!');
                });
        },
        setSubjectUnit(sb_id) {
            axios.get(`/api/course_set/${sb_id}/`)
                .then(() => {
                    window.location.href = '/units';
                })
                .catch(err => {
                    console.error('Грешка:', err);
                    alert('Възникна грешка!');
                });
        },
        loadGoals(logged_user){
            // чета списъка на целите на обучението по предмета по подразбиране на текущия потребител
            const vm = this;
            axios.get('/api/course/'+logged_user.subject+'/goals/')
                .then(function(response){
                    vm.listOfGoals = response.data
                    vm.clearEditMode()
                })
        },
        editGoal(idx){
            this.goal.id = this.listOfGoals[idx].id
            this.goal.num = this.listOfGoals[idx].num
            this.goal.name = this.listOfGoals[idx].name
            this.goal.course = this.listOfGoals[idx].course
            this.setEditMode(0,idx)
        },
        newGoal(){
            this.goal.id = 0
            this.goal.num = this.listOfGoals.length+1
            this.goal.name = ''
            this.goal.course = this.user.subject
            this.setEditMode(0,-1)
        },
        saveGoal() {
            vm = this
            vm.clearEditMode()
            // Изпращане на POST заявка към API
            axios.post('api/goals/upsert/', vm.goal, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                }
            })
                .then(function(response) {
                    vm.loadGoals(vm.user)
                    // Показване на съобщение за успех
                    alert("Данните са записани успешно!");
                })
                .catch(function(error) {
                    alert("Възникна грешка при запазване на данните!");
                });
        },

        loadUnits(logged_user){
            // чета списъка на целите на обучението по предмета по подразбиране на текущия потребител
            const vm = this;
            vm.clearEditMode()
            axios.get(`/api/subjects/${vm.user.subject}/units-with-topics/`)
                .then(function(response){
                    vm.listOfUnits = response.data;
                    console.log('listOfUnits:',vm.listOfUnits)
                })
        },
        saveUnit() {
            console.log('saveUnit()')
            const vm = this;
            vm.clearEditMode()
            axios.post('/api/units/upsert/', vm.unit, {
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }
            })
                .then(() => {
                    // презареди списъка на units+topics за избрания предмет
                    return axios.get(`/api/subjects/${vm.user.subject}/units-with-topics/`);
                })
                .then(resp => {
                    vm.listOfUnits = resp.data; // ако държиш такъв списък

                    alert('Разделът е записан успешно!');
                })
                .catch(() => alert('Грешка при запис на раздел!'));
        },
        newUnit(){
            this.unit.id = 0
            this.unit.num = this.listOfUnits.length+1
            this.unit.name = ''
            this.unit.hours = 1
            this.unit.subject = this.user.subject
            this.setEditMode(0,-1)
        },
        edit_Unit(idx){
            this.unit.id = this.listOfUnits[idx].id
            this.unit.num = this.listOfUnits[idx].num
            this.unit.name = this.listOfUnits[idx].name
            this.unit.hours = this.listOfUnits[idx].hours
            this.unit.subject = this.user.subject
            this.setEditMode(0,idx)
        },

        saveTopic() {
            const vm = this;
            vm.clearEditMode();

            const payload = {
                id: Number(vm.topic.id || 0),
                num: Number(vm.topic.num),
                name: vm.topic.name,
                MoSCoW_cat: vm.topic.MoSCoW_cat,
                MoSCoW_rem: vm.topic.MoSCoW_rem ?? '',
                unit: Number(vm.topic.unit) // гарантирано число
            };

            axios.post('/api/topics/upsert/', payload, {
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }
            })
                .then(() => axios.get(`/api/subjects/${vm.user.subject}/units-with-topics/`))
                .then(resp => {
                    vm.listOfUnits = resp.data;
                    alert('Темата е записана успешно!');
                })
                .catch(err => {
                    console.error('saveTopic error:', err?.response?.data || err);
                    alert('Грешка при запис на тема!');
                });
        },
        newTopic(unit_idx){
            this.topic.id = 0
            this.topic.num = this.listOfUnits[unit_idx].topics.length+1
            this.topic.name = ''
            this.topic.MoSCoW_cat = 'M'
            this.topic.MoSCoW_rem = ''
            this.topic.unit = this.listOfUnits[unit_idx].id
            this.setEditMode(1,-1)
        },
        edit_Topic(unit_idx, idx){
            const unit = this.listOfUnits[unit_idx];
            const topic = unit.topics[idx];

            this.topic.id = topic.id;
            this.topic.num = topic.num;
            this.topic.name = topic.name;
            this.topic.MoSCoW_cat = topic.MoSCoW_cat;
            this.topic.MoSCoW_rem = topic.MoSCoW_rem;

            // Ключова промяна:
            this.topic.unit = unit.id; // не topic.unit

            this.setEditMode(1, idx);
        },

        getTotalHours() {
            if (!Array.isArray(this.listOfUnits)) return 0;
            return this.listOfUnits.reduce((sum, u) => {
                const h = Number(u?.hours ?? 0);
                return sum + (isNaN(h) ? 0 : h);
            }, 0);
        },
        getCurrentSubjectHPY() {
            if (!Array.isArray(this.listOfSubjects)) return null;

            // Уеднаквяване на типовете за сравнение (число)
            const targetId = Number(this.user?.subject);
            if (Number.isNaN(targetId)) return null;

            const subj = this.listOfSubjects.find(s => Number(s?.id) === targetId);
            return subj?.hpy ?? null; // връща hpy или null, ако не е намерен
        },
    },
    created: function(){
        this.status = 0
        this.loadUserDetails();
    }
}

Vue.createApp(App).mount('#main_app')
