/* Project Analysis Chart */
var options = {
    series: [{
        name: 'Active Projects',
        type: 'column',
        data: [1.8, 2.5, 2.5, 1.5, 2.5, 2.8, 3.8]
    }, {
        name: 'Completed Projects',
        type: 'column',
        data: [1.1, 2.2, 3.1, 4, 4.1, 4.9, 6.5]
    }, {
        name: 'Projects Revenue',
        type: 'line',
        data: [20, 29, 37, 35, 44, 43, 50],
    },
    ],
    chart: {
        toolbar: {
            show: false
        },
        height: 327,
        type: 'line',
        stacked: false,
        fontFamily: 'Poppins, Arial, sans-serif',
    },
    grid: {
        borderColor: '#f5f4f4',
        strokeDashArray: 3
    },
    dataLabels: {
        enabled: false
    },
    title: {
        text: undefined,
    },
    xaxis: {
        categories: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    },
    yaxis: [
        {
            show: true,
            axisTicks: {
                show: true,
            },
            axisBorder: {
                show: false,
                color: '#4eb6d0'
            },
            labels: {
                style: {
                    colors: '#4eb6d0',
                }
            },
            title: {
                text: undefined,
            },
            tooltip: {
                enabled: true
            }
        },
        {
            seriesName: 'Completed Projects',
            opposite: true,
            axisTicks: {
                show: true,
            },
            axisBorder: {
                show: false,
            },
            labels: {
                style: {
                    colors: '#00E396',
                }
            },
            title: {
                text: undefined,
            },
        },
        {
            seriesName: 'Projects Revenue',
            opposite: true,
            axisTicks: {
                show: true,
            },
            axisBorder: {
                show: false,
            },
            labels: {
                show: false,
            },
            title: {
                text: undefined,
            }
        },
    ],
    tooltip: {
        enabled: true,
    },
    legend: {
        show: true,
        position: 'top',
        offsetX: 40,
        fontSize: '13px',
        fontWeight: 'normal',
        labels: {
            colors: '#acb1b1',
        },
        markers: {
            width: 10,
            height: 10,
        },
    },
    stroke: {
        width: [0, 0, 1.5],
        curve: 'straight',
        dashArray: [0, 0, 0],
    },
    plotOptions: {
        bar: {
            columnWidth: "35%",
            borderRadius: 3
        }
    },
    colors: ["rgb(46, 144, 250)", "#B2DDFF", "#F79009"]
};
document.querySelector("#projectAnalysis").innerHTML = " ";
var chart1 = new ApexCharts(document.querySelector("#projectAnalysis"), options);
chart1.render();
function projectAnalysis() {
    chart1.updateOptions({
        colors: ["rgb(" + myVarVal + ")", "##2E90FA", "#F79009"],
    })
}
/* Project Analysis Chart */

/* for user1 */
var spark1Options = {
    chart: {
        type: 'line',
        height: 20,
        width: 80,
        sparkline: {
            enabled: true
        },
        dropShadow: {
            enabled: true,
            enabledOnSeries: undefined,
            top: 0,
            left: 0,
            blur: 3,
            color: '#000',
            opacity: 0.1
        }
    },
    grid: {
        show: false,
        xaxis: {
            lines: {
                show: false
            }
        },
        yaxis: {
            lines: {
                show: false
            }
        },
    },
    stroke: {
        show: true,
        curve: 'smooth',
        lineCap: 'butt',
        colors: undefined,
        width: 1.5,
        dashArray: 0,
    },
    fill: {
        gradient: {
            enabled: false
        }
    },
    series: [{
        name: 'Value',
        data: [54, 38, 56, 24, 65]
    }],
    yaxis: {
        min: 0,
        show: false,
        axisBorder: {
            show: false
        }
    },
    xaxis: {
        show: false,
        axisTicks: {
            show: false
        },
        axisBorder: {
            show: false
        }
    },
    colors: ['#09ad95']
};

var spark1El = document.querySelector("#user1");
if (spark1El) {
    spark1El.innerHTML = ''; // remove old chart
    var spark1Chart = new ApexCharts(spark1El, spark1Options);
    spark1Chart.render();
}

/* for user1 */

/* for user2 */
var spark2Options = {
    chart: {
        type: 'line',
        height: 20,
        width: 80,
        sparkline: {
            enabled: true
        },
        dropShadow: {
            enabled: true,
            enabledOnSeries: undefined,
            top: 0,
            left: 0,
            blur: 3,
            color: '#000',
            opacity: 0.1
        }
    },
    grid: {
        show: false,
        xaxis: {
            lines: {
                show: false
            }
        },
        yaxis: {
            lines: {
                show: false
            }
        },
    },
    stroke: {
        show: true,
        curve: 'smooth',
        lineCap: 'butt',
        colors: undefined,
        width: 1.5,
        dashArray: 0,
    },
    fill: {
        gradient: {
            enabled: false
        }
    },
    series: [{
        name: 'Value',
        data: [24, 54, 15, 42, 16]
    }],
    yaxis: {
        min: 0,
        show: false,
        axisBorder: {
            show: false
        }
    },
    xaxis: {
        show: false,
        axisTicks: {
            show: false
        },
        axisBorder: {
            show: false
        }
    },
    colors: ['#fb6b27']
};

var spark2El = document.querySelector("#user2");
if (spark2El) {
    spark2El.innerHTML = ''; // remove old chart
    var spark2Chart = new ApexCharts(spark2El, spark2Options);
    spark2Chart.render();
}

/* for user2 */

/* for user3 */
var spark3Options = {
    chart: {
        type: 'line',
        height: 20,
        width: 80,
        sparkline: {
            enabled: true
        },
        dropShadow: {
            enabled: true,
            enabledOnSeries: undefined,
            top: 0,
            left: 0,
            blur: 3,
            color: '#000',
            opacity: 0.1
        }
    },
    grid: {
        show: false,
        xaxis: {
            lines: {
                show: false
            }
        },
        yaxis: {
            lines: {
                show: false
            }
        },
    },
    stroke: {
        show: true,
        curve: 'smooth',
        lineCap: 'butt',
        colors: undefined,
        width: 1.5,
        dashArray: 0,
    },
    fill: {
        gradient: {
            enabled: false
        }
    },
    series: [{
        name: 'Value',
        data: [15, 42, 16, 44, 24]
    }],
    yaxis: {
        min: 0,
        show: false,
        axisBorder: {
            show: false
        }
    },
    xaxis: {
        show: false,
        axisTicks: {
            show: false
        },
        axisBorder: {
            show: false
        }
    },
    colors: ['#1170e4']
};

var spark3El = document.querySelector("#user3");
if (spark3El) {
    spark3El.innerHTML = ''; // clear previous chart
    var spark3Chart = new ApexCharts(spark3El, spark3Options);
    spark3Chart.render();
}

/* for user3 */

/* for user4 */
var spark4Options = {
    chart: {
        type: 'line',
        height: 20,
        width: 80,
        sparkline: {
            enabled: true
        },
        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 3,
            color: '#000',
            opacity: 0.1
        }
    },
    grid: {
        show: false
    },
    stroke: {
        curve: 'smooth',
        width: 1.5
    },
    fill: {
        gradient: {
            enabled: false
        }
    },
    series: [{
        name: 'Value',
        data: [54, 38, 56, 24, 65]
    }],
    xaxis: {
        show: false,
        axisTicks: {
            show: false
        },
        axisBorder: {
            show: false
        }
    },
    yaxis: {
        min: 0,
        show: false,
        axisBorder: {
            show: false
        }
    },
    colors: ['#e82646']
};

var user4El = document.getElementById('user4');
if (user4El) {
    user4El.innerHTML = ''; // Clear existing chart
    var spark4Chart = new ApexCharts(user4El, spark4Options);
    spark4Chart.render();
} else {
}


/* for user4 */

/* for user5 */
var spark5Options = {
    chart: {
        type: 'line',
        height: 20,
        width: 80,
        sparkline: {
            enabled: true
        },
        dropShadow: {
            enabled: true,
            top: 0,
            left: 0,
            blur: 3,
            color: '#000',
            opacity: 0.1
        }
    },
    grid: {
        show: false
    },
    stroke: {
        curve: 'smooth',
        width: 1.5
    },
    fill: {
        gradient: {
            enabled: false
        }
    },
    series: [{
        name: 'Value',
        data: [15, 42, 16, 44, 24]
    }],
    xaxis: {
        show: false,
        axisTicks: { show: false },
        axisBorder: { show: false }
    },
    yaxis: {
        min: 0,
        show: false,
        axisBorder: { show: false }
    },
    colors: ['#f7b731']
};

var user5El = document.getElementById('user5');

if (user5El) {
    user5El.innerHTML = '';
    var spark5Chart = new ApexCharts(user5El, spark5Options);
    spark5Chart.render();
} else {
}


/* for user5 */