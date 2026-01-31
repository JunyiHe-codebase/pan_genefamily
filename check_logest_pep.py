# -*- coding: utf-8 -*-
# @time    : 2026/01/31 13:53
# @author  : HeJunyi
# @file    : check_longest_pep.py

import argparse
import textwrap


def extract_longest_seq(gene_id_list, seq_dict):
    out_gene_dict = {}
    for gene in gene_id_list:
        if gene in seq_dict:
            # 使用max函数更简洁地找到最长序列
            longest_seq = max(seq_dict[gene], key=len)
            out_gene_dict[gene] = longest_seq
    return out_gene_dict


def run(gene_list_file: str, fasta_file: str, output_file: str):
    # 读取基因列表
    gene_name_list = []
    with open(gene_list_file, 'r') as gene_list:
        for line in gene_list:
            gene_name_list.append(line.strip())

    # 读取FASTA文件
    seq_dict = {}
    current_id = None
    current_seq_parts = []
    
    with open(fasta_file, "r") as fasta_f:
        for line in fasta_f:
            line = line.strip()
            if not line:  # 跳过空行
                continue
            
            if line.startswith(">" ):
                # 如果当前有正在处理的序列，保存它
                if current_id is not None:
                    full_seq = "".join(current_seq_parts)
                    if current_id not in seq_dict:
                        seq_dict[current_id] = []
                    seq_dict[current_id].append(full_seq)
                
                # 开始处理新的序列
                current_id = line[1:].strip()
                current_seq_parts = []
            else:
                # 继续添加当前序列的部分
                current_seq_parts.append(line)
    
    # 保存最后一个序列
    if current_id is not None:
        full_seq = "".join(current_seq_parts)
        if current_id not in seq_dict:
            seq_dict[current_id] = []
        seq_dict[current_id].append(full_seq)

    # 提取最长序列
    out_gene_dict = extract_longest_seq(gene_name_list, seq_dict)

    # 输出结果
    with open(output_file, "w") as out_f:
        for k, v in out_gene_dict.items():
            out_f.write(f">{k}\n")
            out_f.write(textwrap.fill(v, width=80))
            out_f.write("\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--gene_list_file', type=str, required=True,
                        help='Input the gene list file.')
    parser.add_argument('-f', '--fasta_file', type=str, required=True,
                        help='Input the fasta file.')
    parser.add_argument('-o', '--output_file', type=str, required=True,
                        help='Input the output file name.')
    args = parser.parse_args()

    run(args.gene_list_file, args.fasta_file, args.output_file)
    