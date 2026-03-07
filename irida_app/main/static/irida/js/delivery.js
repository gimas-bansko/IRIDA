// ако ползваш Vue 3 от CDN, markRaw е налично на Vue.markRaw
const markRaw = (typeof Vue !== 'undefined' && Vue.markRaw) ? Vue.markRaw : (x) => x;

const App = {
    delimiters: ['[[', ']]'], // Променяме синтаксиса на [[ ]]
    data() {
        return {
            menu_item:'Провеждане на урок',
            user:{},
            session:{},
            topics:[],
            points:[],
            // редакция/добавяне

            moscowMap: {
                M: 'Задължителна тема',
                S: 'Важно, но не критично',
                C: 'Пожелателно',
                W: 'Не влиза, Отпада'
            },
            notes: [],
            tasks: [],

            // task edit
            taskEditMode: false,
            taskForm: { id: 0, session: null, point: null, num: 1, name: '', condition: '', answer: '' },

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
                    vm.loadSessionTopics()
                    vm.loadSessionPoints()
                    vm.loadSessionNotes();
                    vm.loadSessionTasks();                })
        },
        loadSessionTopics() {
            // чета списъка на всички теми, включени в дадено занятие
            const vm = this;
            axios.get('/api/sessions/' + vm.session.id + '/topics/')
                .then(function (response) {
                    vm.topics = response.data
                })
        },
        loadSessionPoints() {
            const vm = this;
            axios.get('/api/sessions/' + vm.session.id + '/points/')
                .then(function (response) {
                    vm.points = response.data
                })
        },
        moscowTextFor(topic) {
            const code = topic?.MoSCoW_cat
            return this.moscowMap[code] || code || ''
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

        // UI helpers
        sanitize(html) {
            // Премахни изображенията като доп. защита, ако желаеш:
            // return DOMPurify.sanitize(html, {FORBID_TAGS: ['img', 'svg']});
            return DOMPurify.sanitize(html);
        },

        // Point
        getTotalMinutes() {
            if (!Array.isArray(this.points)) return 0;
            return this.points.reduce((sum, u) => {
                const m = Number(u?.duration ?? 0);
                return sum + (isNaN(m) ? 0 : m);
            }, 0);
        },
        checkTiming(){
            console.log(this.session.duration*45-this.getTotalMinutes())
            return this.session.duration*45-this.getTotalMinutes()
        },
//*******************************************************
        // Loaders
        loadSessionNotes() {
            const vm = this;
            axios.get('/api/sessions/' + vm.session.id + '/notes/')
                .then(res => {
                    vm.notes = res.data
                    vm.addCollapsedToNotes();
                });
        },
        loadSessionTasks() {
            const vm = this;
            axios.get('/api/sessions/' + vm.session.id + '/tasks/')
                .then(res => {
                    vm.tasks = res.data;
                    vm.addCollapsedToTasks();
                });
        },

        // Notes
        addCollapsedToNotes() {
            if (!Array.isArray(this.notes)) return;
            for (const n of this.notes) {
                if (n && typeof n === 'object' && !Object.prototype.hasOwnProperty.call(n, 'collapsed')) {
                    n.collapsed = true;
                }
            }
        },
        getPointNumNameById(id) {
            if (!Array.isArray(this.points) || id == null) return null;
            const pointId = Number(id);
            const p = this.points.find(pt => Number(pt.id) === pointId);
            if (!p) return null;
            return `към точка ${p.num}. ${p.name}`
        },

        // Tasks
        addCollapsedToTasks() {
            if (!Array.isArray(this.notes)) return;
            for (const n of this.tasks) {
                if (n && typeof n === 'object' && !Object.prototype.hasOwnProperty.call(n, 'collapsed')) {
                    n.collapsed = true;
                }
            }
        },
    },
    created: function(){
        this.loadUserDetails();
    }
}

Vue.createApp(App).mount('#main_app')
