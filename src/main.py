import os
import argparse
from input_parser import parse_input_text
from ppt_generator import generate_presentation
from template_manager import load_template, get_layout_mapping, print_layouts
from layout_manager import LayoutManager
from config import Config
from utils.logger import LOG  # 引入 LOG 模块
import gradio as gr
from agents.idea_agent import IdeaAgent

# 定义主函数，处理输入并生成 PowerPoint 演示文稿
def geneate_pptfile(input_text):
    config = Config()  # 加载配置文件

    ideaAgent = IdeaAgent()

    idea_response = ideaAgent.chat_with_history(input_text)
    # 加载 PowerPoint 模板，并打印模板中的可用布局
    prs = load_template(config.ppt_template)  # 加载模板文件
    LOG.info("可用的幻灯片布局:")  # 记录信息日志，打印可用布局
    print_layouts(prs)  # 打印模板中的布局

    # 初始化 LayoutManager，使用配置文件中的 layout_mapping
    layout_manager = LayoutManager(config.layout_mapping)

    # 调用 parse_input_text 函数，解析输入文本，生成 PowerPoint 数据结构
    powerpoint_data, presentation_title = parse_input_text(idea_response, layout_manager)

    LOG.info(f"解析转换后的 ChatPPT PowerPoint 数据结构:\n{powerpoint_data}")  # 记录调试日志，打印解析后的 PowerPoint 数据

    # 定义输出 PowerPoint 文件的路径
    output_pptx = f"outputs/{presentation_title}.pptx"
    
    # 调用 generate_presentation 函数生成 PowerPoint 演示文稿
    return generate_presentation(powerpoint_data, config.ppt_template, output_pptx)

def main():
    # 使用解析后的输入文件参数运行主函数
    # 使用 Gradio 构建交互界面
    with gr.Blocks(title="从 markdown 文件生成 PowerPoint 演示文稿。") as chatppt_app:
        topic = gr.Textbox(label="Topic")
        output = gr.Textbox(label="File Path")
        generate_btn = gr.Button("Generate File")
        # Attach the generate_file function to the button click event.
        generate_btn.click(fn=geneate_pptfile, inputs=topic, outputs=output, api_name="generate_file")

    chatppt_app.launch(share=True, server_name="0.0.0.0")

# 程序入口
if __name__ == "__main__":
    main()