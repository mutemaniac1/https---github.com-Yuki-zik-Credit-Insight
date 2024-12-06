<template>
  <div>
    <div id="statistics">
      <div id="chart-container">
        <div id="chart" style="width: 400px; height: 390px;"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  mounted() {
    this.initChart();
  },
  methods: {
    initChart() {
      this.chart = echarts.init(document.getElementById('chart')); // 初始化图表实例
      this.setChartOptions();
    },
    setChartOptions() {
      const option = {
        title: {
          text: '服务访问top次数统计',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
  type: 'category',
  data: [
    'te26',
    'jzw',
    'te27',
    'fut13',
    'gis_5',
    'fut4',
    'xz_47',
    'bg'
  ].reverse(),
  axisLabel: {
    overflow: 'truncate', // 标签溢出处理
    ellipsis: true,
    width: 200 // 标签宽度
  }
},

        series: [
          {
            name: '访问次数',
            type: 'bar',
            data: [10, 11, 11, 16, 18, 20, 30, 92].reverse(),
            itemStyle: {
              normal: {
                color: '#66c2ff',
                barBorderRadius: 5
              },
              emphasis: {
                color: '#40a9ff',
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            label: {
              show: true,
              position: 'right'
            }
          }
        ]
      };
      if (this.chart) {
        this.chart.setOption(option); // 设置图表选项
      }
    },
}
}
</script>

<style scoped>


#chart-container {
  position: relative;
  
}


</style>
