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
      required: true
    },
    period: {
      type: String,
      required: true
    }
  },
  setup(props) {
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

      // 根據不同時間範圍設置不同的 x 軸配置
      const xAxisConfig = {
        type: 'category',
        boundaryGap: true,
        data: dates,
        axisLabel: {
          interval: props.period === '月' ? 2 : props.period === '日' ? 1 : 0,  // 月視圖每隔2個，日視圖每隔1個
          rotate: props.period === '月' ? 45 : props.period === '日' ? 45 : 0,  // 月視圖和日視圖都旋轉45度
          fontSize: 11,
          formatter: (value) => {
            if (props.period === '月') {
              // 將 YYYY-MM-DD 格式轉換為 MM/DD 格式
              const date = value.split('-')
              return `${date[1]}/${date[2]}`
            }
            if (props.period === '日') {
              // 只顯示小時，移除 :00
              return value.replace(':00', '')
            }
            return value
          }
        }
      }

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: props.period === '日' ? '10%' : '15%',  // 日視圖底部空間可以小一點
          top: '10%',
          containLabel: true
        },
        xAxis: xAxisConfig,
        yAxis: {
          type: 'value',
          minInterval: 1,
          splitLine: {
            show: true,
            lineStyle: {
              type: 'dashed',
              color: '#ddd'
            }
          }
        },
        series: [
          {
            type: 'bar',
            name: '活躍用戶',
            data: values,
            itemStyle: {
              color: '#3B82F6'
            },
            barWidth: '40%',
            barGap: '30%'
          }
        ]
      }

      console.log('Setting chart option:', option)
      chart.setOption(option)
    }

    onMounted(() => {
      initChart()
      updateChart()
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