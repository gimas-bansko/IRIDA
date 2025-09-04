/* Target Incomplete Chart */
    /* basic bar chart */
 
var options = {
    chart: {
        height: 127,
        width: 100,
        type: "radialBar",
    },

    series: [48],
    colors: ["rgba(255,255,255,0.9)"],
    plotOptions: {
        radialBar: {
            hollow: {
                margin: 0,
                size: "55%",
                background: "#fff"
            },
            dataLabels: {
                name: {
                    offsetY: 10,
                    color: "#4b9bfa",
                    fontSize: ".625rem",
                    show: false
                },
                value: {
                    offsetY: 5,
                    color: "#4b9bfa",
                    fontSize: ".875rem",
                    show: true,
                    fontWeight: 600
                }
            }
        }
    },
    stroke: {
        lineCap: "round"
    },
    labels: ["Status"]
};
document.addEventListener("DOMContentLoaded", function () {
  const crmMain = document.querySelector("#crm-main");
  if (crmMain) {
    crmMain.innerHTML = "";
    var chart = new ApexCharts(crmMain, options);
    chart.render();
  } else {
  }
});


/* Target Incomplete Chart */

/* Total Customers chart */
var crm1Options = {
    chart: {
        type: 'line',
        height: 40,
        width: 100,
        sparkline: {
            enabled: true
        }
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
        type: 'gradient',
        gradient: {
            opacityFrom: 0.9,
            opacityTo: 0.9,
            stops: [0, 98],
        }
    },
    series: [{
        name: 'Value',
        data: [20, 14, 19, 10, 23, 20, 22, 9, 12]
    }],
    yaxis: {
        min: 0,
        show: false,
        axisBorder: {
            show: false
        },
    },
    xaxis: {
        show: false,
        axisBorder: {
            show: false
        },
    },
    tooltip: {
        enabled: false,
    },
    colors: ["rgb(200, 193, 42)"],
};

document.addEventListener("DOMContentLoaded", function () {
  var container = document.getElementById('crm-total-customers');
  if (container) {
    container.innerHTML = ''; // clear previous chart
    var crm1Chart = new ApexCharts(container, crm1Options);
    crm1Chart.render();
  }
});



function crmtotalCustomers() {
    crm1.updateOptions({
        colors: ["rgb(" + myVarVal + ")"],
    });
}
/* Total Customers chart */

/* Total revenue chart */
var crm2Options = {
    chart: {
        type: 'line',
        height: 40,
        width: 100,
        sparkline: {
            enabled: true
        }
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
        type: 'gradient',
        gradient: {
            opacityFrom: 0.9,
            opacityTo: 0.9,
            stops: [0, 98],
        }
    },
    series: [{
        name: 'Value',
        data: [20, 14, 20, 22, 9, 12, 19, 10, 25]
    }],
    yaxis: {
        min: 0,
        show: false,
        axisBorder: {
            show: false
        },
    },
    xaxis: {
        show: false,
        axisBorder: {
            show: false
        },
    },
    tooltip: {
        enabled: false,
    },
    colors: ["rgb(247, 144, 9)"]
};

document.addEventListener("DOMContentLoaded", function () {
    var revenueEl = document.getElementById('crm-total-revenue');

    if (revenueEl) {
        revenueEl.innerHTML = '';
        var crm2Chart = new ApexCharts(revenueEl, crm2Options);
        crm2Chart.render();
    }
});


/* Total revenue chart */

/* Conversion ratio Chart */
var crm3Options = {
    chart: {
        type: 'line',
        height: 40,
        width: 100,
        sparkline: {
            enabled: true
        }
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
        type: 'gradient',
        gradient: {
            opacityFrom: 0.9,
            opacityTo: 0.9,
            stops: [0, 98],
        }
    },
    series: [{
        name: 'Value',
        data: [20, 20, 22, 9, 14, 19, 10, 25, 12]
    }],
    yaxis: {
        min: 0,
        show: false,
        axisBorder: {
            show: false
        },
    },
    xaxis: {
        show: false,
        axisBorder: {
            show: false
        },
    },
    tooltip: {
        enabled: false,
    },
    colors: ["rgb(38, 191, 148)"]
};

document.addEventListener("DOMContentLoaded", function () {
    var ratioEl = document.getElementById('crm-conversion-ratio');

    if (ratioEl) {
        ratioEl.innerHTML = '';
        var crm3Chart = new ApexCharts(ratioEl, crm3Options);
        crm3Chart.render();
    }
});


/* Conversion ratio Chart */

/* Total Deals Chart */
var crm4Options = {
    chart: {
        type: 'line',
        height: 40,
        width: 100,
        sparkline: {
            enabled: true
        }
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
        type: 'gradient',
        gradient: {
            opacityFrom: 0.9,
            opacityTo: 0.9,
            stops: [0, 98],
        }
    },
    series: [{
        name: 'Value',
        data: [20, 20, 22, 9, 12, 14, 19, 10, 25]
    }],
    yaxis: {
        min: 0,
        show: false,
        axisBorder: {
            show: false
        },
    },
    xaxis: {
        show: false,
        axisBorder: {
            show: false
        },
    },
    tooltip: {
        enabled: false,
    },
    colors: ["rgb(0, 38, 255)"]
};

document.addEventListener("DOMContentLoaded", function () {
    var el = document.getElementById('crm-total-deals');
    if (el) {
        el.innerHTML = '';
        var crm4Chart = new ApexCharts(el, crm4Options);
        crm4Chart.render();
    }
});


/* Total Deals Chart */

/* Revenue Analytics Chart */
var options = {
    series: [
        {
            type: 'line',
            name: 'Profit',
            data: [
                {
                    x: 'Jan',
                    y: 100
                },
                {
                    x: 'Feb',
                    y: 210
                },
                {
                    x: 'Mar',
                    y: 180
                },
                {
                    x: 'Apr',
                    y: 454
                },
                {
                    x: 'May',
                    y: 230
                },
                {
                    x: 'Jun',
                    y: 320
                },
                {
                    x: 'Jul',
                    y: 656
                },
                {
                    x: 'Aug',
                    y: 830
                },
                {
                    x: 'Sep',
                    y: 350
                },
                {
                    x: 'Oct',
                    y: 350
                },
                {
                    x: 'Nov',
                    y: 210
                },
                {
                    x: 'Dec',
                    y: 410
                }
            ]
        },
        {
            type: 'line',
            name: 'Revenue',
            chart: {
                dropShadow: {
                    enabled: true,
                    enabledOnSeries: undefined,
                    top: 5,
                    left: 0,
                    blur: 3,
                    color: '#000',
                    opacity: 0.1
                }
            },
            data: [
                {
                    x: 'Jan',
                    y: 180
                },
                {
                    x: 'Feb',
                    y: 620
                },
                {
                    x: 'Mar',
                    y: 476
                },
                {
                    x: 'Apr',
                    y: 220
                },
                {
                    x: 'May',
                    y: 520
                },
                {
                    x: 'Jun',
                    y: 780
                },
                {
                    x: 'Jul',
                    y: 435
                },
                {
                    x: 'Aug',
                    y: 515
                },
                {
                    x: 'Sep',
                    y: 738
                },
                {
                    x: 'Oct',
                    y: 454
                },
                {
                    x: 'Nov',
                    y: 525
                },
                {
                    x: 'Dec',
                    y: 230
                }
            ]
        },
        {
            type: 'area',
            name: 'Sales',
            chart: {
                dropShadow: {
                    enabled: true,
                    enabledOnSeries: undefined,
                    top: 5,
                    left: 0,
                    blur: 3,
                    color: '#000',
                    opacity: 0.1
                }
            },
            data: [
                {
                    x: 'Jan',
                    y: 200
                },
                {
                    x: 'Feb',
                    y: 530
                },
                {
                    x: 'Mar',
                    y: 110
                },
                {
                    x: 'Apr',
                    y: 130
                },
                {
                    x: 'May',
                    y: 480
                },
                {
                    x: 'Jun',
                    y: 520
                },
                {
                    x: 'Jul',
                    y: 780
                },
                {
                    x: 'Aug',
                    y: 435
                },
                {
                    x: 'Sep',
                    y: 475
                },
                {
                    x: 'Oct',
                    y: 738
                },
                {
                    x: 'Nov',
                    y: 454
                },
                {
                    x: 'Dec',
                    y: 480
                }
            ]
        }
    ],
    chart: {
        height: 350,
        animations: {
            speed: 500
        },
        dropShadow: {
            enabled: true,
            enabledOnSeries: undefined,
            top: 8,
            left: 0,
            blur: 3,
            color: '#000',
            opacity: 0.1
        },
    },
    colors: ["rgb(132, 90, 223)", "rgba(35, 183, 229, 0.85)", "rgba(119, 119, 142, 0.05)"],
    dataLabels: {
        enabled: false
    },
    grid: {
        borderColor: '#f1f1f1',
        strokeDashArray: 3
    },
    stroke: {
        curve: 'smooth',
        width: [2, 2, 0],
        dashArray: [0, 5, 0],
    },
    xaxis: {
        axisTicks: {
            show: false,
        },
    },
    yaxis: {
        labels: {
            formatter: function (value) {
                return "$" + value;
            }
        },
    },
    tooltip: {
        y: [{
            formatter: function(e) {
                return void 0 !== e ? "$" + e.toFixed(0) : e
            }
        }, {
            formatter: function(e) {
                return void 0 !== e ? "$" + e.toFixed(0) : e
            }
        }, {
            formatter: function(e) {
                return void 0 !== e ? e.toFixed(0) : e
            }
        }]
    },
    legend: {
        show: true,
        customLegendItems: ['Profit', 'Revenue', 'Sales'],
        inverseOrder: true
    },
    title: {
        text: 'Revenue Analytics with sales & profit (USD)',
        align: 'left',
        style: {
            fontSize: '.8125rem',
            fontWeight: 'semibold',
            color: '#8c9097'
        },
    },
    markers: {
        hover: {
            sizeOffset: 5
        }
    }
};
var el = document.getElementById('crm-revenue-analytics');
if (el) {
    el.innerHTML = '';
    var chart = new ApexCharts(el, options);
    chart.render();
}


function revenueAnalytics() {
    chart.updateOptions({
        colors: ["rgba(" + myVarVal + ", 1)", "rgba(35, 183, 229, 0.85)", "rgba(119, 119, 142, 0.05)"],
    });
}
/* Revenue Analytics Chart */

/* Profits Earned Chart */
var options1 = {
    series: [{
        name: 'Profit Earned',
        data: [44, 42, 57, 86, 58, 55, 70],
    }, {
        name: 'Total Sales',
        data: [34, 22, 37, 56, 21, 35, 60],
    }],
    chart: {
        type: 'bar',
        height: 284,
        toolbar: {
            show: false,
        }
    },
    grid: {
        borderColor: '#f1f1f1',
        strokeDashArray: 3
        
    },
    colors: function({ seriesIndex, dataPointIndex }) {
        if(seriesIndex === 0 && dataPointIndex === 0) {
            return 'rgb(0, 0, 255)';  // blue color for first bar of first series
        }
        if(seriesIndex === 0) {
            return "rgb(132, 90, 223)";
        } else {
            return "#e4e7ed";
        }
    },
    plotOptions: {
        bar: {
            borderRadius: 10,
            columnWidth: '60%',
        }
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        show: true,
        width: 2,
        colors: undefined,
    },
    legend: {
        show: false,
        position: 'top',
    },
    yaxis: {
        title: {
            style: {
                color: '#fff',
                fontSize: '13px',
                fontFamily: 'poppins, sans-serif',
                fontWeight: 600,
                cssClass: 'apexcharts-yaxis-label',
            },
        },
        labels: {
            formatter: function (y) {
                return y.toFixed(0) + "";
            }
        }
    },
    xaxis: {
        categories: [ 'Mon','Tue', 'Wed', 'Thu', 'Fri', 'Sat','Sun'],
        axisBorder: {
            show: true,
            color: '#888',
            offsetX: 0,
            offsetY: 0,
        },
        axisTicks: {
            show: true,
            borderType: 'solid',
            color: '#fff',
            width: 6,
            offsetX: 0,
            offsetY: 0
        },
        labels: {
            rotate: -90
        }
    }
};

document.addEventListener('DOMContentLoaded', function () {
  var el = document.getElementById('crm-profits-earned');
  if (el) {
    el.innerHTML = '';
    var chart1 = new ApexCharts(el, options1);
    chart1.render();
  }
});


function crmProfitsearned() {
    chart1.updateOptions({
        colors: ["rgba(" + myVarVal + ", 1)", "#ededed"],
    });
}
/* Profits Earned Chart */

/* Leads By Source Chart */
Chart.defaults.elements.arc.borderWidth = 0;
Chart.defaults.datasets.doughnut.cutout = '85%';
var chartInstance = new Chart(document.getElementById("leads-source"), {
    type: 'doughnut',
    data: {
        datasets: [{
            label: 'My First Dataset',
            data: [32, 27, 25, 16],
            backgroundColor: [
                'rgb(132, 90, 223)',
                'rgb(35, 183, 229)',
                'rgb(38, 191, 148)',
                'rgb(245, 184, 73)',
            ]
        }]
    },
    plugins: [{
        afterUpdate: function (chart) {
            const arcs = chart.getDatasetMeta(0).data;

            arcs.forEach(function (arc) {
                arc.round = {
                    x: (chart.chartArea.left + chart.chartArea.right) / 2,
                    y: (chart.chartArea.top + chart.chartArea.bottom) / 2,
                    radius: (arc.outerRadius + arc.innerRadius) / 2,
                    thickness: (arc.outerRadius - arc.innerRadius) / 2,
                    backgroundColor: arc.options.backgroundColor
                }
            });
        },
        afterDraw: (chart) => {
            const {
                ctx,
                canvas
            } = chart;

            chart.getDatasetMeta(0).data.forEach(arc => {
                const startAngle = Math.PI / 2 - arc.startAngle;
                const endAngle = Math.PI / 2 - arc.endAngle;

                ctx.save();
                ctx.translate(arc.round.x, arc.round.y);
                ctx.fillStyle = arc.options.backgroundColor;
                ctx.beginPath();
                ctx.arc(arc.round.radius * Math.sin(endAngle), arc.round.radius * Math.cos(endAngle), arc.round.thickness, 0, 2 * Math.PI);
                ctx.closePath();
                ctx.fill();
                ctx.restore();
            });
        }
    }]
});

function leads(myVarVal) {

    chartInstance.data.datasets[0] = {
        label: 'My First Dataset',
        data: [32, 27, 25, 16],
        backgroundColor: [
            `rgb(${myVarVal})`,
            'rgb(35, 183, 229)',
            'rgb(245, 184, 73)',
            'rgb(38, 191, 148)',
        ]
    }
    chartInstance.update();

}
/* Leads By Source Chart */


