<template>
  <div ref="chartContainer" style="width: 100%; height: 600px"></div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

export default {
  name: 'LineChart',
  props: {
    data: {
      type: Object,
      required: true,
      default: () => ({
        dates: [],
        values: [],
        newUsers: [],
        activityRate: []
      })
    },
    period: {
      type: String,
      required: true,
      default: '月'  // 設置預設值為"月"
    }
  },
  setup(props, { emit }) {
    const chartContainer = ref(null)
    let chart = null

    const initChart = () => {
      if (chartContainer.value && !chart) {
        chart = echarts.init(chartContainer.value)
        window.addEventListener('resize', () => {
          chart.resize()
        })
      }
    }

    const updateChart = () => {
      if (!chart || !props.data || !props.data.dates || !props.data.values) {
        console.log('Missing data or chart:', { chart, data: props.data })
        return
      }

      const { dates, values } = props.data
      console.log('Updating chart with:', { dates, values })

      // 根據不同時間範圍設置標題和軸標籤
      // - 日：最近24小時
      // - 週：當日減7天 (T-7)
      // - 月：當日減30天 (T-30)
      const periodText = {
        '日': '24小時',
        '週': '一週',
        '月': '30天'
      }[props.period]

      const xAxisConfig = {
        type: 'category',
        boundaryGap: true,
        data: dates,
        name: '時間',
        nameLocation: 'middle',
        nameGap: 35,
        axisLabel: {
          interval: props.period === '月' ? 'auto' : 0,
          rotate: props.period === '月' ? 45 : 0,
          fontSize: 11,
          formatter: (value) => {
            if (!value) return '';
            if (props.period === '月') {
              return value;
            }
            if (props.period === '週') {
              const date = new Date(value)
              return `${date.getMonth() + 1}/${date.getDate()}`
            }
            if (props.period === '日') {
              return value.replace(':00', '')
            }
            return value
          }
        }
      }

      const option = {
        title: {
          text: `最近${periodText}用戶活躍度統計`,
          left: 'center',
          top: 0,
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          formatter: function(params) {
            let result = params[0].name + '<br/>';
            params.forEach(param => {
              if (param.value > 0) {  // 只顯示有數值的項目
                const marker = param.marker;
                const value = param.value;
                const unit = param.seriesName === '平均活躍度' ? '%' : ' 人';
                result += marker + param.seriesName + ': ' + value + unit + '<br/>';
              }
            });
            return result;
          }
        },
        legend: {
          data: ['活躍用戶數', '新增用戶數', '平均活躍度'],
          bottom: 0
        },
        grid: {
          left: '3%',
          right: '5%',  // 稍微增加右側空間以容納標籤
          bottom: '15%',
          top: '15%',
          containLabel: true
        },
        xAxis: xAxisConfig,
        yAxis: [
          {
            type: 'value',
            name: '用戶數 (人)',
            nameLocation: 'middle',
            nameGap: 50,
            nameTextStyle: {
              padding: [0, 0, 0, 50],  // 增加左側padding
              color: '#666'
            },
            minInterval: 1,
            axisLabel: {
              color: '#666',
              fontSize: 12,
              margin: 16
            },
            splitLine: {
              show: true,
              lineStyle: {
                type: 'dashed',
                color: '#ddd'
              }
            }
          },
          {
            type: 'value',
            name: '活躍度 (%)',
            nameLocation: 'middle',
            nameGap: 50,
            nameTextStyle: {
              padding: [0, 50, 0, 0],  // 增加右側padding
              color: '#666'
            },
            min: 0,
            max: 100,
            interval: 20,
            axisLabel: {
              color: '#666',
              fontSize: 12,
              margin: 16,
              formatter: '{value}%'
            },
            splitLine: {
              show: false
            }
          }
        ],
        series: [
          {
            type: 'bar',
            name: '活躍用戶數',
            data: values.map(v => v > 0 ? v : '-'),  // 將0值轉換為'-'
            itemStyle: {
              color: '#3B82F6'
            },
            barWidth: '30%',
            barGap: '0%',
            label: {
              show: true,
              position: 'top',
              formatter: function(params) {
                return params.value > 0 ? `${params.value}` : '';
              },
              fontSize: 12,
              color: '#3B82F6',
              backgroundColor: 'rgba(255, 255, 255, 0.9)',
              borderColor: '#3B82F6',
              borderWidth: 1,
              borderRadius: 4,
              padding: [2, 4],
              distance: 4
            }
          },
          {
            type: 'bar',
            name: '新增用戶數',
            data: values.map(v => {
              const val = Math.round(v * 0.3);
              return val > 0 ? val : '-';
            }),
            itemStyle: {
              color: '#10B981'
            },
            barWidth: '30%',
            label: {
              show: true,
              position: 'top',
              formatter: function(params) {
                return params.value > 0 ? `${params.value}` : '';
              },
              fontSize: 12,
              color: '#10B981',
              backgroundColor: 'rgba(255, 255, 255, 0.9)',
              borderColor: '#10B981',
              borderWidth: 1,
              borderRadius: 4,
              padding: [2, 4],
              distance: 4
            }
          },
          {
            type: 'line',
            name: '平均活躍度',
            yAxisIndex: 1,
            data: values.map(v => {
              const val = Math.round(v * 15);
              return val > 0 ? val : '-';
            }),
            itemStyle: {
              color: '#F59E0B'
            },
            symbol: 'circle',
            symbolSize: 6,
            showSymbol: true,
            connectNulls: false,  // 不連接空值點
            smooth: true,
            label: {
              show: true,
              position: 'top',
              formatter: function(params) {
                return params.value > 0 ? `${params.value}%` : '';
              },
              fontSize: 12,
              color: '#F59E0B',
              backgroundColor: 'rgba(255, 255, 255, 0.9)',
              borderColor: '#F59E0B',
              borderWidth: 1,
              borderRadius: 4,
              padding: [2, 4],
              distance: 4
            }
          }
        ]
      }

      console.log('Setting chart option:', option)
      chart.setOption(option)
    }

    onMounted(() => {
      initChart()
      updateChart()
      // 在組件掛載時發出事件，設置預設值為"月"
      emit('update:period', '月')
    })

    onUnmounted(() => {
      if (chart) {
        chart.dispose()
        window.removeEventListener('resize', () => chart.resize())
      }
    })

    watch(() => props.data, updateChart, { deep: true })
    watch(() => props.period, updateChart)

    return {
      chartContainer
    }
  }
}
</script> 