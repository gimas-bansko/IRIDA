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
                timing: false,
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

            // часовник
            currentTime: '',

            // конфигурация на учебния ден
            schoolDayStart: '20:00',
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
            return Math.max(min, Math.min(max, value));
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
            const num = Number(value);
            return isNaN(num) ? fallback : num;
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
            if (this.selectedPointNum == null) return null;
            return this.points.find(p => Number(p?.num) === Number(this.selectedPointNum)) || null;
        },

        getSelectedPointSortedIndex() {
            const sortedPoints = this.getSortedPoints();
            if (!sortedPoints.length || this.selectedPointNum == null) return -1;

            return sortedPoints.findIndex(p => Number(p?.num) === Number(this.selectedPointNum));
        },

        getPointByNum(pointNum) {
            if (pointNum == null) return null;
            return this.points.find(p => Number(p?.num) === Number(pointNum)) || null;
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

            this.showSelectedPointContent.timing = false;
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
            const sortedPoints = this.getSortedPoints();
            const targetNum = Number(selectedPointNum);
            let sum = 0;
            for (const p of sortedPoints) {
                if (Number(p.num) >= targetNum) break;
                sum += this.toNumberSafe(p.duration, 0) * 60;
            }
            return sum;
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
                    vm.loadSessionTasks();
                })
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
            if (!Array.isArray(this.tasks)) return;
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
            const timeline = [];
            const startDate = this.parseStartTimeToTodayDate();
            let cursor = new Date(startDate);

            for (let lessonNum = 1; lessonNum <= this.schoolLessonsCount; lessonNum++) {
                const lessonStart = new Date(cursor);
                const lessonEnd = new Date(cursor.getTime() + this.lessonDurationSeconds * 1000);

                timeline.push({
                    type: 'lesson',
                    lessonNumber: lessonNum,
                    startDate: lessonStart,
                    endDate: lessonEnd,
                    durationSeconds: this.lessonDurationSeconds
                });

                cursor = lessonEnd;

                if (lessonNum < this.schoolLessonsCount) {
                    const breakDuration = lessonNum === 1 ? this.firstBreakDurationSeconds : this.regularBreakDurationSeconds;
                    const breakStart = new Date(cursor);
                    const breakEnd = new Date(cursor.getTime() + breakDuration * 1000);

                    timeline.push({
                        type: 'break',
                        breakAfterLesson: lessonNum,
                        nextLessonNumber: lessonNum + 1,
                        startDate: breakStart,
                        endDate: breakEnd,
                        durationSeconds: breakDuration
                    });

                    cursor = breakEnd;
                }
            }

            return timeline;
        },

        getCurrentSchoolInterval(now = new Date()) {
        const timeline = this.buildSchoolTimeline();
            for (const interval of timeline) {
                if (now >= interval.startDate && now < interval.endDate) {
                    return interval;
                }
            }
            return null;
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
            const interval = this.getCurrentSchoolInterval(now);
            if (!interval) return null;

            if (interval.type === 'lesson') {
                return {
                    lessonNumber: interval.lessonNumber,
                    startDate: interval.startDate,
                    mode: 'lesson'
                };
            }

            if (interval.type === 'break') {
                const timeline = this.buildSchoolTimeline();
                const nextLesson = timeline.find(i => i.type === 'lesson' && i.lessonNumber === interval.nextLessonNumber);
                if (nextLesson) {
                    return {
                        lessonNumber: nextLesson.lessonNumber,
                        startDate: nextLesson.startDate,
                        mode: 'break'
                    };
                }
            }

            return null;
        },

        // =====================================================
        // ЕФЕКТИВНО УЧЕБНО ВРЕМЕ (БЕЗ МЕЖДУЧАСИЯ)
        // =====================================================

        getEffectiveLessonSecondsBetween(startDate, endDate) {
            if (startDate >= endDate) return 0;

            const timeline = this.buildSchoolTimeline();
            let effectiveSeconds = 0;

            for (const interval of timeline) {
                if (interval.type !== 'lesson') continue;

                const overlapStart = startDate > interval.startDate ? startDate : interval.startDate;
                const overlapEnd = endDate < interval.endDate ? endDate : interval.endDate;

                if (overlapStart < overlapEnd) {
                    effectiveSeconds += Math.floor((overlapEnd - overlapStart) / 1000);
                }
            }

            return effectiveSeconds;
        },

        addEffectiveLessonSeconds(startDate, secondsToAdd) {
        if (secondsToAdd <= 0) return new Date(startDate);

            const timeline = this.buildSchoolTimeline();
            let remaining = secondsToAdd;
            let cursor = new Date(startDate);

            for (const interval of timeline) {
                if (interval.type !== 'lesson') continue;
                if (cursor >= interval.endDate) continue;

                const effectiveStart = cursor > interval.startDate ? cursor : interval.startDate;
                const availableSeconds = Math.floor((interval.endDate - effectiveStart) / 1000);

                if (remaining <= availableSeconds) {
                    return new Date(effectiveStart.getTime() + remaining * 1000);
                }

                remaining -= availableSeconds;
                cursor = interval.endDate;
            }

            return new Date(cursor.getTime() + remaining * 1000);
        },

        isDateInsideLessonInterval(date) {
        const timeline = this.buildSchoolTimeline();
            for (const interval of timeline) {
                if (interval.type === 'lesson' && date >= interval.startDate && date < interval.endDate) {
                    return true;
                }
            }
            return false;
        },

        isDateInsideBreakInterval(date) {
        const timeline = this.buildSchoolTimeline();
            for (const interval of timeline) {
                if (interval.type === 'break' && date >= interval.startDate && date < interval.endDate) {
                    return true;
                }
            }
            return false;
        },

        // =====================================================
        // СТАРТ / СТОП / RESET НА УРОК
        // =====================================================

        initializeLessonPlanningState() {
            this.lessonRun.totalPlannedSeconds = this.toNumberSafe(this.session.duration, 0) * 45 * 60;
            this.resetLessonRun();
        },

        startLesson() {
        const anchor = this.getLessonAnchorForStart();
            if (!anchor) {
                alert('Не можете да стартирате урок извън учебното време');
                return;
            }

            this.lessonRun.started = true;
            this.lessonRun.paused = false;
            this.lessonRun.startedAt = new Date();
            this.lessonRun.anchoredLessonNumber = anchor.lessonNumber;
            this.lessonRun.anchoredLessonStartDate = anchor.startDate;
            this.lessonRun.anchoredStartMode = anchor.mode;
            this.lessonRun.totalPlannedSeconds = this.toNumberSafe(this.session.duration, 0) * 45 * 60;

            this.updateLessonRunTiming();
            this.updateSelectedPointTiming();
            this.startLessonTimingTicker();
        },

        stopLesson() {
        this.lessonRun.started = false;
            this.lessonRun.paused = false;
            this.stopLessonTimingTicker();
            this.resetLessonRun();
        },

        pauseLesson() {
        if (!this.lessonRun.started) return;
            this.lessonRun.paused = true;
            this.stopLessonTimingTicker();
        },

        resumeLesson() {
        if (!this.lessonRun.started || !this.lessonRun.paused) return;
            this.lessonRun.paused = false;
            this.startLessonTimingTicker();
        },

        resetLessonRun() {
            this.lessonRun.started = false;
                this.lessonRun.paused = false;
                this.lessonRun.startedAt = null;
                this.lessonRun.anchoredLessonNumber = null;
                this.lessonRun.anchoredLessonStartDate = null;
                this.lessonRun.anchoredStartMode = 'lesson';
                this.lessonRun.totalElapsedSeconds = 0;
                this.lessonRun.totalRemainingSeconds = 0;
                this.lessonRun.totalOverdueSeconds = 0;
                this.lessonRun.totalElapsed = '00:00';
                this.lessonRun.totalRemaining = '00:00';
                this.lessonRun.totalOverdue = '00:00';
                this.lessonRun.status = 'idle';

                this.pointTiming.pointNum = null;
                this.pointTiming.pointName = '';
                this.pointTiming.pointPlannedSeconds = 0;
                this.pointTiming.pointPlannedStartOffsetSeconds = 0;
                this.pointTiming.pointPlannedEndOffsetSeconds = 0;
                this.pointTiming.pointPlannedStartDate = null;
                this.pointTiming.pointPlannedEndDate = null;
                this.pointTiming.pointElapsedSeconds = 0;
                this.pointTiming.pointRemainingSeconds = 0;
                this.pointTiming.pointOverdueSeconds = 0;
                this.pointTiming.pointElapsed = '00:00';
                this.pointTiming.pointRemaining = '00:00';
                this.pointTiming.pointOverdue = '00:00';
                this.pointTiming.pointElapsedPercentage = 0;
                this.pointTiming.status = 'idle';
            },

        // =====================================================
        // ТАЙМИНГ НА УРОКА
        // =====================================================

        updateLessonRunTiming(now = new Date()) {
            if (!this.lessonRun.started || !this.lessonRun.anchoredLessonStartDate) {
                this.lessonRun.status = 'idle';
                return;
            }

            const elapsed = this.getEffectiveLessonSecondsBetween(this.lessonRun.anchoredLessonStartDate, now);
            this.lessonRun.totalElapsedSeconds = elapsed;
            this.lessonRun.totalElapsed = this.formatMMSS(elapsed);

            if (elapsed < this.lessonRun.totalPlannedSeconds) {
                this.lessonRun.totalRemainingSeconds = this.lessonRun.totalPlannedSeconds - elapsed;
                this.lessonRun.totalRemaining = this.formatMMSS(this.lessonRun.totalRemainingSeconds);
                this.lessonRun.totalOverdueSeconds = 0;
                this.lessonRun.totalOverdue = '00:00';

                if (this.lessonRun.anchoredStartMode === 'break' && now < this.lessonRun.anchoredLessonStartDate) {
                    this.lessonRun.status = 'waiting';
                } else {
                    this.lessonRun.status = 'running';
                }
            } else if (elapsed === this.lessonRun.totalPlannedSeconds) {
                this.lessonRun.totalRemainingSeconds = 0;
                this.lessonRun.totalRemaining = '00:00';
                this.lessonRun.totalOverdueSeconds = 0;
                this.lessonRun.totalOverdue = '00:00';
                this.lessonRun.status = 'finished';
            } else {
                this.lessonRun.totalRemainingSeconds = 0;
                this.lessonRun.totalRemaining = '00:00';
                this.lessonRun.totalOverdueSeconds = elapsed - this.lessonRun.totalPlannedSeconds;
                this.lessonRun.totalOverdue = this.formatMMSS(this.lessonRun.totalOverdueSeconds);
                this.lessonRun.status = 'overtime';
            }
        },

        getLessonPlannedEndDate() {
            if (!this.lessonRun.anchoredLessonStartDate) return null;
                return this.addEffectiveLessonSeconds(
                    this.lessonRun.anchoredLessonStartDate,
                    this.lessonRun.totalPlannedSeconds
                );
            },

        isLessonCurrentlyPausedByBreak(now = new Date()) {
            if (!this.lessonRun.started) return false;
                return this.isDateInsideBreakInterval(now);
            },

        // =====================================================
        // ТАЙМИНГ НА ТЕКУЩАТА ТОЧКА
        // =====================================================

        updateSelectedPointTiming(now = new Date()) {
            const point = this.getSelectedPoint();
            if (!point || !this.lessonRun.started || !this.lessonRun.anchoredLessonStartDate) {
                this.pointTiming.status = 'idle';
                return;
            }

            this.pointTiming.pointNum = point.num;
            this.pointTiming.pointName = point.name || '';
            this.pointTiming.pointPlannedSeconds = this.toNumberSafe(point.duration, 0) * 60;

            const previousSeconds = this.getPreviousPointsDurationSeconds(point.num);
            this.pointTiming.pointPlannedStartOffsetSeconds = previousSeconds;
            this.pointTiming.pointPlannedEndOffsetSeconds = previousSeconds + this.pointTiming.pointPlannedSeconds;

            this.pointTiming.pointPlannedStartDate = this.getSelectedPointPlannedStartDate();
            this.pointTiming.pointPlannedEndDate = this.getSelectedPointPlannedEndDate();

            const elapsed = this.getEffectiveLessonSecondsBetween(this.lessonRun.anchoredLessonStartDate, now);

            if (elapsed < this.pointTiming.pointPlannedStartOffsetSeconds) {
                this.pointTiming.status = 'upcoming';
                this.pointTiming.pointElapsedSeconds = 0;
                this.pointTiming.pointRemainingSeconds = this.pointTiming.pointPlannedSeconds;
                this.pointTiming.pointOverdueSeconds = 0;
            } else if (elapsed < this.pointTiming.pointPlannedEndOffsetSeconds) {
                this.pointTiming.status = 'current';
                this.pointTiming.pointElapsedSeconds = elapsed - this.pointTiming.pointPlannedStartOffsetSeconds;
                this.pointTiming.pointRemainingSeconds = this.pointTiming.pointPlannedSeconds - this.pointTiming.pointElapsedSeconds;
                this.pointTiming.pointOverdueSeconds = 0;
            } else {
                const overdue = elapsed - this.pointTiming.pointPlannedEndOffsetSeconds;
                if (overdue > 0) {
                    this.pointTiming.status = 'overdue';
                    this.pointTiming.pointElapsedSeconds = this.pointTiming.pointPlannedSeconds + overdue;
                    this.pointTiming.pointRemainingSeconds = 0;
                    this.pointTiming.pointOverdueSeconds = overdue;
                } else {
                    this.pointTiming.status = 'finished';
                    this.pointTiming.pointElapsedSeconds = this.pointTiming.pointPlannedSeconds;
                    this.pointTiming.pointRemainingSeconds = 0;
                    this.pointTiming.pointOverdueSeconds = 0;
                }
            }

            this.pointTiming.pointElapsed = this.formatMMSS(this.pointTiming.pointElapsedSeconds);
            this.pointTiming.pointRemaining = this.formatMMSS(this.pointTiming.pointRemainingSeconds);
            this.pointTiming.pointOverdue = this.formatMMSS(this.pointTiming.pointOverdueSeconds);

            if (this.pointTiming.pointPlannedSeconds > 0) {
                this.pointTiming.pointElapsedPercentage = Math.floor(
                    (this.pointTiming.pointElapsedSeconds / this.pointTiming.pointPlannedSeconds) * 100
                );
            } else {
                this.pointTiming.pointElapsedPercentage = 0;
            }
        },

        getSelectedPointPlannedStartDate() {
            if (!this.lessonRun.anchoredLessonStartDate) return null;
                return this.addEffectiveLessonSeconds(
                    this.lessonRun.anchoredLessonStartDate,
                    this.pointTiming.pointPlannedStartOffsetSeconds
                );
            },

        getSelectedPointPlannedEndDate() {
            if (!this.lessonRun.anchoredLessonStartDate) return null;
                return this.addEffectiveLessonSeconds(
                    this.lessonRun.anchoredLessonStartDate,
                    this.pointTiming.pointPlannedEndOffsetSeconds
                );
            },

        getSelectedPointTimingStatus(now = new Date()) {
            if (!this.lessonRun.started || !this.lessonRun.anchoredLessonStartDate) return 'idle';

                const elapsed = this.getEffectiveLessonSecondsBetween(this.lessonRun.anchoredLessonStartDate, now);

                if (elapsed < this.pointTiming.pointPlannedStartOffsetSeconds) return 'upcoming';
                if (elapsed < this.pointTiming.pointPlannedEndOffsetSeconds) return 'current';
                if (elapsed === this.pointTiming.pointPlannedEndOffsetSeconds) return 'finished';
                return 'overdue';
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
            this.updateCurrentTime();
            if (this.lessonRun.started && !this.lessonRun.paused) {
                this.updateLessonRunTiming();
                this.updateSelectedPointTiming();
            }
        },

        startClock() {
            if (this._clockInterval) return;
                this.updateCurrentTime();
                this._clockInterval = setInterval(() => {
                    this.tickClockAndTiming();
                }, 1000);
            },

        stopClock() {
            if (this._clockInterval) {
                clearInterval(this._clockInterval);
                this._clockInterval = null;
            }
            },

        startLessonTimingTicker() {
            if (this._lessonTimingInterval) return;
                this._lessonTimingInterval = setInterval(() => {
                    if (this.lessonRun.started && !this.lessonRun.paused) {
                        this.updateLessonRunTiming();
                        this.updateSelectedPointTiming();
                    }
                }, 1000);
            },

        stopLessonTimingTicker() {
            if (this._lessonTimingInterval) {
                clearInterval(this._lessonTimingInterval);
                this._lessonTimingInterval = null;
            }
            },
    },
    created() {
        this.loadUserDetails();
        this.startClock();
    },
    beforeUnmount() {
        this.stopClock();
        this.stopLessonTimingTicker();
    }
};


Vue.createApp(App).mount('#main_app')
