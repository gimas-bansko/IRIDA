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

            selectedPointNum: null,
            minPointNum: null,
            maxPointNum: null,
            selectedPointPosition: 'empty',
            pointRefs: [],
            showSelectedPointContent: {
                content: false,
                notes: false,
                tasks: false,
                tests: false,
                attachments: false,
            },

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

            // време
            currentTime: '',
            schoolDayStart: '08:00',
            scheduleInfo: {
                state: 'before',
                lessonNumber: null,
                breakAfterLesson: null,
                elapsed: '00:00',
                remaining: '00:00'
            },
        }
    },
    computed: {
    },
    methods: {
        getSortedPoints() {
            if (!Array.isArray(this.points)) return [];

            return [...this.points].sort((a, b) => {
                return Number(a?.num ?? 0) - Number(b?.num ?? 0);
            });
        },
        getSelectedPointSortedIndex() {
            const sortedPoints = this.getSortedPoints();
            if (!sortedPoints.length || this.selectedPointNum == null) return -1;

            return sortedPoints.findIndex(p => Number(p?.num) === Number(this.selectedPointNum));
        },
        updatePointNumBounds() {
            const sortedPoints = this.getSortedPoints();

            if (!sortedPoints.length) {
                this.minPointNum = null;
                this.maxPointNum = null;
                return;
            }

            this.minPointNum = Number(sortedPoints[0].num);
            this.maxPointNum = Number(sortedPoints[sortedPoints.length - 1].num);
        },
        updateSelectedPointPosition() {
            const sortedPoints = this.getSortedPoints();

            if (!sortedPoints.length) {
                this.selectedPointNum = null;
                this.selectedPointPosition = 'empty';
                this.minPointNum = null;
                this.maxPointNum = null;
                return;
            }

            this.showSelectedPointContent.content = false;
            this.showSelectedPointContent.notes = false;
            this.showSelectedPointContent.tasks = false;
            this.showSelectedPointContent.tests = false;
            this.showSelectedPointContent.attachments = false;

            this.updatePointNumBounds();

            const selectedSortedIndex = this.getSelectedPointSortedIndex();

            if (selectedSortedIndex === -1) {
                this.selectedPointNum = Number(sortedPoints[0].num);
                this.selectedPointPosition = 'first';
                return;
            }

            if (selectedSortedIndex === 0) {
                this.selectedPointPosition = 'first';
                return;
            }

            if (selectedSortedIndex === sortedPoints.length - 1) {
                this.selectedPointPosition = 'last';
                return;
            }

            this.selectedPointPosition = 'middle';
        },
        setPointRef(el, index) {
            if (el) {
                this.pointRefs[index] = el;
            }
        },
        scrollToSelectedPoint() {
            this.$nextTick(() => {
                const container = this.$refs.pointsContainer;
                const el = this.pointRefs[this.selectedPointNum];
                if (!el) return;

                if (!container || !el) return;

                const offset = el.offsetHeight + 300;

                container.scrollTo({
                    top: el.offsetTop - container.offsetTop - offset,
                    behavior: 'smooth'
                });
            });
        },
        nextSelectedPoint() {
            const sortedPoints = this.getSortedPoints();

            if (!sortedPoints.length) {
                this.updateSelectedPointPosition();
                return;
            }

            const selectedSortedIndex = this.getSelectedPointSortedIndex();

            if (selectedSortedIndex === -1) {
                this.selectedPointNum = Number(sortedPoints[0].num);
            } else if (selectedSortedIndex < sortedPoints.length - 1) {
                this.selectedPointNum = Number(sortedPoints[selectedSortedIndex + 1].num);
            }

            this.updateSelectedPointPosition();
            this.scrollToSelectedPoint();
        },
        prevSelectedPoint() {
            const sortedPoints = this.getSortedPoints();

            if (!sortedPoints.length) {
                this.updateSelectedPointPosition();
                return;
            }

            const selectedSortedIndex = this.getSelectedPointSortedIndex();

            if (selectedSortedIndex === -1) {
                this.selectedPointNum = Number(sortedPoints[0].num);
            } else if (selectedSortedIndex > 0) {
                this.selectedPointNum = Number(sortedPoints[selectedSortedIndex - 1].num);
            }

            this.updateSelectedPointPosition();
            this.scrollToSelectedPoint();
        },

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
                    vm.updatePointNumBounds();
                    vm.updateSelectedPointPosition();
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
        isSelectedPoint(p) {
            return Number(p?.num) === Number(this.selectedPointNum);
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
        updateCurrentTime() {
            const now = new Date();
    
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
    
            this.currentTime = `${hours}:${minutes}:${seconds}`;
        },
        
    },
    created: function(){
        this.loadUserDetails();
        this.updateCurrentTime();
        this._clockInterval = setInterval(() => {
            this.updateCurrentTime();
        }, 1000);
    },
    beforeUnmount() {
        if (this._clockInterval) {
            clearInterval(this._clockInterval);
        }
    }
}

Vue.createApp(App).mount('#main_app')
