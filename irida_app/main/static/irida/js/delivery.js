// ако ползваш Vue 3 от CDN, markRaw е налично на Vue.markRaw
const markRaw = (typeof Vue !== 'undefined' && Vue.markRaw) ? Vue.markRaw : (x) => x;

const App = {
    delimiters: ['[[', ']]'], // Променяме синтаксиса на [[ ]]
    data() {
        return {
            menu_item: 'Провеждане на урок',

            user: {},
            session: {},
            topics: [],
            points: [],
            notes: [],
            tasks: [],

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

            taskEditMode: false,
            taskForm: {
                id: 0,
                session: null,
                point: null,
                num: 1,
                name: '',
                condition: '',
                answer: ''
            },

            // часовник
            currentTime: '',

            // конфигурация на учебния ден
            schoolDayStart: '08:00',
            schoolLessonsCount: 7,
            lessonDurationSeconds: 45 * 60,
            firstBreakDurationSeconds: 20 * 60,
            regularBreakDurationSeconds: 10 * 60,

            // текущ учебен интервал
            scheduleInfo: {
                state: 'before', // before | lesson | break | after
                lessonNumber: null,
                nextLessonNumber: null,
                breakAfterLesson: null,

                intervalStartDate: null,
                intervalEndDate: null,

                elapsedSeconds: 0,
                remainingSeconds: 0,
                intervalSeconds: 0,
                elapsedPercentage: 0,

                elapsed: '00:00',
                remaining: '00:00'
            },

            // провеждане на урок
            lessonRun: {
                started: false,
                paused: false,

                startedAt: null,               // реален момент на натискане Start
                anchoredLessonNumber: null,    // часът, към който е закачен урокът
                anchoredLessonStartDate: null, // началото на този учебен час
                anchoredStartMode: 'lesson',   // lesson | break

                totalPlannedSeconds: 0,        // session.duration * 45 * 60
                totalElapsedSeconds: 0,
                totalRemainingSeconds: 0,
                totalOverdueSeconds: 0,

                totalElapsed: '00:00',
                totalRemaining: '00:00',
                totalOverdue: '00:00',

                status: 'idle' // idle | waiting | running | finished | overtime
            },

            // тайминг на текущата точка
            pointTiming: {
                pointNum: null,
                pointName: '',

                pointPlannedSeconds: 0,
                pointPlannedStartOffsetSeconds: 0,
                pointPlannedEndOffsetSeconds: 0,

                pointPlannedStartDate: null,
                pointPlannedEndDate: null,

                pointElapsedSeconds: 0,
                pointRemainingSeconds: 0,
                pointOverdueSeconds: 0,

                pointElapsed: '00:00',
                pointRemaining: '00:00',
                pointOverdue: '00:00',

                pointElapsedPercentage: 0,

                status: 'idle' // idle | upcoming | current | overdue | finished
            },

            // служебни таймери
            _clockInterval: null,
            _lessonTimingInterval: null
        }
    },
    computed: {
    sortedPoints() {
        return this.getSortedPoints();
    },

    selectedPoint() {
        return this.getSelectedPoint();
    },

    isLessonRunning() {
        return this.lessonRun.started;
    },

    isLessonWaiting() {
        return this.lessonRun.status === 'waiting';
    },

    isLessonActive() {
        return this.lessonRun.status === 'running';
    },

    isLessonOvertime() {
        return this.lessonRun.status === 'overtime';
    },

    isCurrentPointOverdue() {
        return this.pointTiming.status === 'overdue';
    }
    },
    methods: {
    // =====================================================
    // БАЗОВИ HELPERS
    // =====================================================

    formatMMSS(totalSeconds) {
        const safeSeconds = Math.max(0, Number(totalSeconds) || 0);
        const minutes = String(Math.floor(safeSeconds / 60)).padStart(2, '0');
        const seconds = String(safeSeconds % 60).padStart(2, '0');
        return `${minutes}:${seconds}`;
    },

    clamp(value, min, max) {
        // TODO
    },

    parseStartTimeToTodayDate() {
        const [hours, minutes] = (this.schoolDayStart || '08:00').split(':').map(Number);
        const now = new Date();
        return new Date(
            now.getFullYear(),
            now.getMonth(),
            now.getDate(),
            hours || 0,
            minutes || 0,
            0
        );
    },

    toNumberSafe(value, fallback = 0) {
        // TODO
    },

    // =====================================================
    // POINTS / ИЗБРАНА ТОЧКА
    // =====================================================

    getSortedPoints() {
        if (!Array.isArray(this.points)) return [];

        return [...this.points].sort((a, b) => {
            return Number(a?.num ?? 0) - Number(b?.num ?? 0);
        });
    },

    getSelectedPoint() {
        // TODO
    },

    getSelectedPointSortedIndex() {
        const sortedPoints = this.getSortedPoints();
        if (!sortedPoints.length || this.selectedPointNum == null) return -1;

        return sortedPoints.findIndex(p => Number(p?.num) === Number(this.selectedPointNum));
    },

    getPointByNum(pointNum) {
        // TODO
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
        this.updateSelectedPointTiming();
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
        this.updateSelectedPointTiming();
        this.scrollToSelectedPoint();
    },

    isSelectedPoint(p) {
        return Number(p?.num) === Number(this.selectedPointNum);
    },

    getPreviousPointsDurationSeconds(selectedPointNum) {
        // TODO
        // сбор от duration на предходните точки
    },

    // =====================================================
    // ЗАРЕЖДАНЕ НА ДАННИ
    // =====================================================

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
                vm.initializeLessonPlanningState();
            })
    },

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

    addCollapsedToNotes() {
        if (!Array.isArray(this.notes)) return;
        for (const n of this.notes) {
            if (n && typeof n === 'object' && !Object.prototype.hasOwnProperty.call(n, 'collapsed')) {
                n.collapsed = true;
            }
        }
    },

    addCollapsedToTasks() {
        if (!Array.isArray(this.notes)) return;
        for (const n of this.tasks) {
            if (n && typeof n === 'object' && !Object.prototype.hasOwnProperty.call(n, 'collapsed')) {
                n.collapsed = true;
            }
        }
    },

    // =====================================================
    // UI HELPERS
    // =====================================================

    sanitize(html) {
        // Премахни изображенията като доп. защита, ако желаеш:
        // return DOMPurify.sanitize(html, {FORBID_TAGS: ['img', 'svg']});
        return DOMPurify.sanitize(html);
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

    getPointNumNameById(id) {
        if (!Array.isArray(this.points) || id == null) return null;
        const pointId = Number(id);
        const p = this.points.find(pt => Number(pt.id) === pointId);
        if (!p) return null;
        return `към точка ${p.num}. ${p.name}`
    },

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

    // =====================================================
    // УЧЕБЕН ГРАФИК
    // =====================================================

    buildSchoolTimeline() {
        // TODO
        // връща масив от lesson/break интервали за деня:
        // [
        //   {
        //     type: 'lesson',
        //     lessonNumber: 1,
        //     startDate: Date,
        //     endDate: Date,
        //     durationSeconds: 2700
        //   },
        //   {
        //     type: 'break',
        //     breakAfterLesson: 1,
        //     nextLessonNumber: 2,
        //     startDate: Date,
        //     endDate: Date,
        //     durationSeconds: 1200
        //   }
        // ]
    },

    getCurrentSchoolInterval(now = new Date()) {
        // TODO
        // намира текущия интервал от buildSchoolTimeline()
    },

    updateScheduleInfo() {
        // пълни scheduleInfo на база текущото време
        const startDate = this.parseStartTimeToTodayDate();
        const now = new Date();

        const diffSeconds = Math.floor((now - startDate) / 1000);

        if (diffSeconds < 0) {
            this.scheduleInfo = {
                state: 'before',
                lessonNumber: null,
                breakAfterLesson: null,
                elapsed: '00:00',
                remaining: this.formatMMSS(Math.abs(diffSeconds))
            };
            return;
        }

        const lessonDuration = 45 * 60;
        const firstBreakDuration = 20 * 60;
        const regularBreakDuration = 10 * 60;

        let cursor = 0;
        let lessonNumber = 1;

        while (lessonNumber <= 7) {
            const lessonStart = cursor;
            const lessonEnd = lessonStart + lessonDuration;

            if (diffSeconds >= lessonStart && diffSeconds < lessonEnd) {
                this.scheduleInfo = {
                    state: 'lesson',
                    lessonNumber,
                    breakAfterLesson: null,
                    elapsedSeconds: diffSeconds - lessonStart,
                    remainingSeconds: lessonEnd - diffSeconds,
                    elapsed: this.formatMMSS(diffSeconds - lessonStart),
                    remaining: this.formatMMSS(lessonEnd - diffSeconds),
                    intervalSeconds: lessonDuration,
                    elapsedPercentage: Math.floor((diffSeconds - lessonStart)*100 / lessonDuration),
                };
                return;
            }

            cursor = lessonEnd;

            const breakDuration = lessonNumber === 1 ? firstBreakDuration : regularBreakDuration;
            const breakStart = cursor;
            const breakEnd = breakStart + breakDuration;

            if (diffSeconds >= breakStart && diffSeconds < breakEnd) {
                this.scheduleInfo = {
                    state: 'break',
                    lessonNumber: null,
                    breakAfterLesson: lessonNumber,
                    elapsedSeconds: diffSeconds - breakStart,
                    remainingSeconds: breakEnd - diffSeconds,
                    elapsed: this.formatMMSS(diffSeconds - breakStart),
                    remaining: this.formatMMSS(breakEnd - diffSeconds),
                    intervalSeconds: breakDuration,
                    elapsedPercentage: Math.floor((diffSeconds - breakStart)*100 / breakDuration),
                };
                return;
            }

            cursor = breakEnd;
            lessonNumber += 1;
        }

        this.scheduleInfo = {
            state: 'after',
            lessonNumber: null,
            breakAfterLesson: null,
            elapsed: '00:00',
            remaining: '00:00',
            elapsedSeconds: 0,
            remainingSeconds: 0,
            intervalSeconds: 0,
            elapsedPercentage: 0,
        };
    },

    getLessonAnchorForStart(now = new Date()) {
        // TODO
        // ако е час -> връща текущия час
        // ако е междучасие -> връща следващия час
        // ако няма подходящ -> null
    },

    // =====================================================
    // ЕФЕКТИВНО УЧЕБНО ВРЕМЕ (БЕЗ МЕЖДУЧАСИЯ)
    // =====================================================

    getEffectiveLessonSecondsBetween(startDate, endDate) {
        // TODO
        // връща колко учебни секунди са минали между две дати
        // без да брои междучасията
    },

    addEffectiveLessonSeconds(startDate, secondsToAdd) {
        // TODO
        // добавя само учебно време към дадена дата
        // прескача междучасията
        // връща Date
    },

    isDateInsideLessonInterval(date) {
        // TODO
    },

    isDateInsideBreakInterval(date) {
        // TODO
    },

    // =====================================================
    // СТАРТ / СТОП / RESET НА УРОК
    // =====================================================

    initializeLessonPlanningState() {
        // TODO
        // начална инициализация след зареждане на points/session
        // напр. totalPlannedSeconds, point timing reset и т.н.
    },

    startLesson() {
        // TODO
        // 1. намира anchor чрез getLessonAnchorForStart()
        // 2. записва startedAt, anchoredLessonNumber, anchoredLessonStartDate
        // 3. задава totalPlannedSeconds = session.duration * 45 * 60
        // 4. стартира updateLessonRunTiming()
        // 5. стартира updateSelectedPointTiming()
    },

    stopLesson() {
        // TODO
    },

    pauseLesson() {
        // TODO
    },

    resumeLesson() {
        // TODO
    },

    resetLessonRun() {
        // TODO
        // връща lessonRun и pointTiming в начално състояние
    },

    // =====================================================
    // ТАЙМИНГ НА УРОКА
    // =====================================================

    updateLessonRunTiming(now = new Date()) {
        // TODO
        // смята:
        // totalElapsedSeconds
        // totalRemainingSeconds
        // totalOverdueSeconds
        // status: waiting/running/overtime/finished
    },

    getLessonPlannedEndDate() {
        // TODO
        // anchoredLessonStartDate + totalPlannedSeconds (само учебно време)
    },

    isLessonCurrentlyPausedByBreak(now = new Date()) {
        // TODO
        // ако урокът е стартиран, но в момента е междучасие
    },

    // =====================================================
    // ТАЙМИНГ НА ТЕКУЩАТА ТОЧКА
    // =====================================================

    updateSelectedPointTiming(now = new Date()) {
        // TODO
        // използва selectedPointNum и lessonRun
        // смята планиран старт/край и текущ статус на точката
    },

    getSelectedPointPlannedStartDate() {
        // TODO
    },

    getSelectedPointPlannedEndDate() {
        // TODO
    },

    getSelectedPointTimingStatus(now = new Date()) {
        // TODO
        // upcoming | current | overdue | finished
    },

    // =====================================================
    // CLOCK / TICK
    // =====================================================

    updateCurrentTime() {
        // обновява currentTime
        // и updateScheduleInfo()
        const now = new Date();

        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');

        this.currentTime = `${hours}:${minutes}:${seconds}`;
        this.updateScheduleInfo();
    },

    tickClockAndTiming() {
        // TODO
        // updateCurrentTime()
        // if (lessonRun.started) {
        //   updateLessonRunTiming()
        //   updateSelectedPointTiming()
        // }
    },

    startClock() {
        // TODO
    },

    stopClock() {
        // TODO
    },

    startLessonTimingTicker() {
        // TODO
    },

    stopLessonTimingTicker() {
        // TODO
    },
// ----------------------------------------------------------------------


        // UI helpers

        // Point

//*******************************************************
        // Loaders

        // Notes

        // Tasks


    },
    created() {
        this.loadUserDetails();
        this.startClock();
    },
    beforeUnmount() {
        this.stopClock();
        this.stopLessonTimingTicker();
    },
};


Vue.createApp(App).mount('#main_app')
