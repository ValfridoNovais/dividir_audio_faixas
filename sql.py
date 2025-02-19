import pandas as pd
from datetime import datetime

# Função para converter valores booleanos
def converter_booleano(valor):
    return 'TRUE' if valor == 'Sim' else 'FALSE'

# Função para converter datas
def converter_data(data_str):
    try:
        return datetime.strptime(data_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except:
        return None

# Função para limpar telefones
def limpar_telefone(telefone):
    return ''.join(filter(str.isdigit, str(telefone)))

# Ler o arquivo CSV com codificação 'latin1'
df = pd.read_csv(r"C:\Users\valfr\Downloads\jiujitsu_abisai2.csv", delimiter=';', encoding='latin1')

# Abrir o arquivo SQL para escrita
with open('inserts.sql', 'w', encoding='utf-8') as f:
    for index, row in df.iterrows():
        # Tratar os dados
        nome_aluno = row['  Nome completo do aluno:   '].strip()
        cpf_aluno = row['CPF_Aluno'].strip()
        data_nascimento = converter_data(row['  Data de nascimento:   '].strip())
        telefone_aluno = limpar_telefone(row['  Telefone:  '])
        email = row['EndereÁo de e-mail'].strip()
        rg = row['  RG do aluno: '].strip()
        endereco_aluno = row['  EndereÁo:  '].strip()
        bairro_aluno = None # Não há coluna específica no CSV
        cidade_aluno = None # Não há coluna específica no CSV
        nome_responsavel = row['  Nome Completo do respons·vel:   '].strip()
        tipo_parentesco = row['  Parentesco:   '].strip()
        rg_responsavel = row['  RG do respons·vel:   '].strip()
        cpf_responsavel = row['   CPF do respons·vel:   '].strip()
        telefone_responsavel = limpar_telefone(row['  Telefone do respons·vel:   '])
        telefone_emergencia = limpar_telefone(row['  Telefone  para emergÍncia:   '])
        experiencia_jujitsu = 'TRUE' if 'Veterano' in row['experiencia_jujitsu'] else 'FALSE'
        qual_faixa_atualmente = row['qual_faixa_atualmente'].strip()
        alergico = converter_booleano(row['Possui alergias? '])
        medicamento_controlado = converter_booleano(row['  Utiliza medicamentos de uso contÌnuo? '])
        restricoes_medicas = converter_booleano(row['  Possui restriÁıes mÈdicas?  '])
        ja_sofreu_lesoes_musculares = converter_booleano(row['  J· sofreu lesıes musculares ou Ûsseas?   '])
        ja_sofreu_lesao_ossea = converter_booleano(row['  J· sofreu lesıes musculares ou Ûsseas?   ']) # Mesma coluna
        problemas_respiratorios = converter_booleano(row['  Possui problemas respiratÛrios ou cardÌacos?   '])
        problemas_cardiacos = converter_booleano(row['  Possui problemas respiratÛrios ou cardÌacos?   ']) # Mesma coluna

        # Gerar o comando INSERT
        insert = f"""
        INSERT INTO Cadastro_Matricula (
            nome_aluno, cpf_aluno, data_nascimento, telefone_aluno, email, rg, endereco_aluno, 
            bairro_aluno, cidade_aluno, nome_responsavel, tipo_parentesco, rg_responsavel, 
            cpf_responsavel, telefone_responsavel, telefone_emergencia, experiencia_jujitsu, 
            qual_faixa_atualmente, alergico, medicamento_controlado, restricoes_medicas, 
            ja_sofreu_lesoes_musculares, ja_sofreu_lesao_ossea, problemas_respiratorios, problemas_cardiacos
        ) VALUES (
            '{nome_aluno}', '{cpf_aluno}', '{data_nascimento}', '{telefone_aluno}', '{email}', '{rg}', '{endereco_aluno}', 
            {f"'{bairro_aluno}'" if bairro_aluno else 'NULL'}, {f"'{cidade_aluno}'" if cidade_aluno else 'NULL'}, 
            '{nome_responsavel}', '{tipo_parentesco}', '{rg_responsavel}', '{cpf_responsavel}', 
            '{telefone_responsavel}', '{telefone_emergencia}', {experiencia_jujitsu}, 
            '{qual_faixa_atualmente}', {alergico}, {medicamento_controlado}, {restricoes_medicas}, 
            {ja_sofreu_lesoes_musculares}, {ja_sofreu_lesao_ossea}, {problemas_respiratorios}, {problemas_cardiacos}
        );
        """

        # Escrever no arquivo
        f.write(insert + '\n')

print("Arquivo 'inserts.sql' gerado com sucesso!")