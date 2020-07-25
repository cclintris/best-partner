import React, { Component } from 'react';
import { Input, Button, Divider, Descriptions, message, Modal } from 'antd'
import { CheckOutlined } from '@ant-design/icons'
import axios from 'axios'

export class Start1 extends Component {
    constructor() {
        super()
        this.state = {
            ques_type : '',
            upload_time : '',
            code_similarity : '',
            code_time_complexity : '',
            code_space_complexity : '',
            is_indent_using_one : '',
            is_space_nums_multiple_of_four : '',
            is_within_len_range : '',
            is_not_trailing_space : '',
            is_space_around_operator : '',
            is_not_space_around_operator_in_def : '',
            is_using_one_quotation : '',
            is_not_blank_line_beginning : '',
            is_not_inline_comments : '',
            is_space_after_pound : '',
            is_blank_line_after_import : '',
            is_blank_line_before_class : '',
            is_blank_line_before_def : '',
            is_not_diff_package_in_the_same_line : '',
            is_import_before_from : '',
            is_not_blank_between_import : '',
            is_using_meaningful_name : '',
            code_style_score : '',
            visible : false, // Modal show visible
        }
    }

    showModal = () => {
        this.setState({
            visible : true
        })
    }

    handleOk = e => {
        console.log(e);
        this.setState({
            visible: false,
        });
      };
    
    handleCancel = e => {
        console.log(e);
        this.setState({
            visible: false,
        });
    };

    get_report() {
        let student_id = document.getElementById("student-id")
        let ques_id = document.getElementById("ques-id")
        let student_id_val = String(student_id.value)
        let ques_id_val = String(ques_id.value)
        // console.log('student: ' + student_id_val + ' ' +'ques: ' + ques_id_val)
        axios.get(`http://localhost:5000/report/student_id=${student_id_val}/ques_id=${ques_id_val}`)
        .then(response => {
            let data = response.data
            console.log(data)
            if(data.message === "Invalid Input") {
                message.warning("学生id和题目id不可为空!")
            }else if(data.message === "Valid Input") {
                this.setState({
                    ques_type : data.ques_type,
                    upload_time : data.upload_time,
                    code_similarity : data.code_similarity,
                    code_time_complexity : data.code_time_complexity,
                    code_space_complexity : data.code_space_complexity,
                    is_indent_using_one : data.is_indent_using_one,
                    is_space_nums_multiple_of_four : data.is_space_nums_multiple_of_four,
                    is_within_len_range : data.is_within_len_range,
                    is_not_trailing_space : data.is_not_trailing_space,
                    is_space_around_operator : data.is_space_around_operator,
                    is_not_space_around_operator_in_def : data.is_not_space_around_operator_in_def,
                    is_using_one_quotation : data.is_using_one_quotation,
                    is_not_blank_line_beginning : data.is_not_blank_line_beginning,
                    is_not_inline_comments : data.is_not_inline_comments,
                    is_space_after_pound : data.is_space_after_pound,
                    is_blank_line_after_import : data.is_blank_line_after_import,
                    is_blank_line_before_class : data.is_blank_line_before_class,
                    is_blank_line_before_def : data.is_blank_line_before_def,
                    is_not_diff_package_in_the_same_line : data.is_not_diff_package_in_the_same_line,
                    is_import_before_from : data.is_import_before_from,
                    is_not_blank_between_import : data.is_not_blank_between_import,
                    is_using_meaningful_name : data.is_using_meaningful_name,
                    code_style_score : data.code_style_score,
                })
            }
        })
        .catch(error => {
            console.log(error)
        })
    }

    render() {
        return (
            <div className="startlayout">
                <Input placeholder="请输入学生 id :" id="student-id"></Input>
                <Divider type="vertical"/>
                <Input placeholder="请输入题目 id :" id="ques-id"></Input>
                <Divider type="vertical"/>
                <Button type="primary" 
                        icon={<CheckOutlined />} 
                        onClick={() => this.get_report()}>
                        确认
                </Button>
                <Divider />
                <Descriptions title="学生编程评价报告" bordered className="description-text">
                    <Descriptions.Item label="题目分组">
                        { this.state.ques_type }
                    </Descriptions.Item>
                    <Descriptions.Item label="最后提交时间">
                        { this.state.upload_time }
                    </Descriptions.Item>
                    <Descriptions.Item label="代码相似度">
                        { this.state.code_similarity } %
                    </Descriptions.Item>
                    <Descriptions.Item label="代码时间复杂度">
                        { this.state.code_time_complexity }
                    </Descriptions.Item>
                    <Descriptions.Item label="代码空间复杂度">
                        { this.state.code_space_complexity }
                    </Descriptions.Item>
                    <Descriptions.Item label="代码风格">
                        <Button type="dashed" primary onClick={() => this.showModal()}>查看详情</Button>
                        <Modal
                            title="代码风格详情"
                            visible={ this.state.visible }
                            onOk = { this.handleOk }
                            onCancel = { this.handleCancel }
                        >
                            <h2>分数 : { this.state.code_style_score }</h2>
                            <p>代码是否只是用一种缩进 : { this.state.is_indent_using_one }</p>
                            <p>缩进时，空格数是否是4的倍数 : { this.state.is_space_nums_multiple_of_four }</p>
                            <p>单行代码是否没有超过既定长度 : { this.state.is_within_len_range }</p>
                            <p>代码是否没有尾随空格 : { this.state.is_not_trailing_space }</p>
                            <p>操作符两边是否有空格: { this.state.is_space_around_operator }</p>
                            <p>定义中的操作符两边是否没有空格 : { this.state.is_not_space_around_operator_in_def }</p>
                            <p>是否只使用了一种引号(特殊情况除外) : { this.state.is_using_one_quotation }</p>
                            <p>代码开头是否不是空行 : { this.state.is_not_blank_line_beginning }</p>
                            <p>代码是否没有行内注释 : { this.state.is_not_inline_comments }</p>
                            <p>以"#"开头的注释"#"后是否有空格 : { this.state.is_space_after_pound }</p>
                            <p>在import之后是否有空行 : { this.state.is_blank_line_after_import }</p>
                            <p>在class之前是否有空行 : { this.state.is_blank_line_before_class }</p>
                            <p>在def之前是否有空行: { this.state.is_blank_line_before_def }</p>
                            <p>是否没有在同一行的import导入不同的包 : { this.state.is_not_diff_package_in_the_same_line }</p>
                            <p>用from开头的import是否在其他的import之后 : { this.state.is_import_before_from }</p>
                            <p>import之间是否没有空行 : { this.state.is_not_blank_between_import }</p>
                            <p>变量名命名是否有意义/合理 : { this.state.is_using_meaningful_name }</p>
                        </Modal>
                    </Descriptions.Item>
                </Descriptions>
            </div>
        )
    }
}

export default Start1;
