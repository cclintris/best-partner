import React, { Component } from 'react'
import echarts from 'echarts/lib/echarts'
import ReactEcharts from 'echarts-for-react'

const radarTextStyle = {
    color: '#333',
    fontStyle: 'normal',
    fontWeight: 'normal',
    fontSize: 12,
};


export class Echart extends Component {
    constructor(props) {
        super(props)
        this.state = {
            overall_student_value: [220, 410, 398, 400],
            specific_student_value: [120, 290, 287, 320],
        }
    }

    getOption() {
        return {
            title: {
                text : ''
            },
            legend: {
                data: [
                    { name: '总体软院学生'},
                    { name: '目标学生'}
                ],
                bottom: 0,
                backgroundColor: 'transparent',
                itemWidth: 12,
                itemHeight: 9,
                textStyle: radarTextStyle
            },
            radar: {
                shape: 'polygon',
                splitNumber: 3,
                center: ['50%', '50%'],
                radius: '65%',
                nameGap: 5,
                triggerEvent: true,
                name: {
                    textStyle: {
                        color: '#999',
                        backgroundColor: 'transparent'
                    },
                    formatter: function(value, indicator) {
                        value = value.replace(/\S{4}/g, function(match) {
                            return match + '\n'
                        })
                        return '{a|'+value+'}' + '\n' + '{b|'+indicator.value+'}'
                    },
                    rich: {
                        a: {
                            color: '#999',
                            fontSize: 12,
                            align: 'center'
                        },
                        b: {
                            color: '#333',
                            fontSize: 13,
                            align: 'center'
                        }
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: '#ddd'
                    }
                },
                indicator: [
                    {"name":"代码估计相似度","value":'',"max":500},
                    {"name":"代码时间复杂度","value":'',"max":500},
                    {"name":"代码风格水平","value":'',"max":500},
                    {"name":"代码空间复杂度","value":'',"max":500},
                ],
                splitArea: {
                    show: false,
                    areaStyle: {
                        color: 'rgba(255,0,0,0)'
                    }
                }
            },
            series: [{
                name: '代码質量',
                type: 'radar',
                areaStyle: {normal: {}},
                data: [
                    {
                        value: this.state.overall_student_value,
                        itemStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0.5,
                                    color: 'rgba(48, 107, 231, 1)'
                                },{
                                    offset: 1,
                                    color: 'rgba(73, 168, 255, 0.7)'
                                }]),
                                opacity: 0,
                                lineStyle: {
                                    width: 0,
                                    color: '#306BE7'
                                },
                            },
                        },
                        name: '总体软院学生',
                        id: 'overall_student'
                    },
                    {
                        value: this.state.specific_student_value,
                        itemStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0.5,
                                    color: 'rgba(139, 241, 134, 0.7)'
                                },{
                                    offset: 1,
                                    color: 'rgba(0, 208, 131, 1)'
                                }]),
                                opacity: 0,
                                lineStyle: {
                                    width: 0,
                                    color: '#8BF186'
                                },
                            },
                        },
                        name: '目标学生',
                        id: 'specific_student'
                    }
                ]
            }]
        }
    }

    onChartClick(param) {
        console.log(param)
    }

    onChartLegendselectchanged(param) {
        console.log(param)
    }

    render () {
        let onEvents = {
            'click': this.onChartClick.bind(this),
            'legendselectchanged': this.onChartLegendselectchanged.bind(this)
        }
        return (
            <div className="echartsRadar">
                <ReactEcharts 
                    option={this.getOption()}
                    notMerge={true}
                    lazyUpdate={true}
                    onEvents={onEvents}
                    style={{width: '100%', height: '100%'}}
                />
            </div>
        )
    }
}

export default Echart
