import pandas as pd
import numpy as np
from neo4j.v1 import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "mjgh2765"))

def extract_qa(df,graph_name):
    #df = pd.read_excel(file_data,sheet_name='QA_Pairs')
    df = df.replace(np.nan, '', regex=True)
    df.replace({r'\A\s+|\s+\Z': '', '\n': ' ', "'": ''}, regex=True, inplace=True)

    df['question_query'] = ""
    df['intent_query'] = ""
    df['entities_query'] = ""
    df['response_query'] = ""

    df['edge1_query'] = ""
    df['edge2_query'] = ""
    df['edge3_query'] = ""


    for index, row in df.iterrows():
        df.loc[index, 'question_query'] = "MERGE(n2:%s:Question {content:'%s',q_id:'%s'})" % (graph_name, row['Question'], row['Q Number'])
        df.loc[index, 'intent_query'] = "MERGE(n2:%s:Intent {name:'%s', question:'%s'})" % (graph_name, row['Intent'], row['Question'])
        df.loc[index, 'entities_query'] = "MERGE(n2:%s:Entities {values:'%s', intent:'%s'})" % (graph_name, row['Entities'], row['Intent'])
        df.loc[index, 'response_query'] = "MERGE(n2:%s:Response {content:'%s'})" % (graph_name, row['Answer'])

        df.loc[index, 'edge1_query'] = "MATCH (n1:%s:Question {content:'%s'}),(n2:%s:Intent {name:'%s', question:'%s'}) MERGE (n1)-[r:HAS_INTENT]->(n2)" % (graph_name, row['Question'], graph_name, row['Intent'], row['Question'])
        df.loc[index, 'edge2_query'] = "MATCH (n1:%s:Intent {name:'%s', question:'%s'}),(n2:%s:Entities {values:'%s', intent:'%s'}) MERGE (n1)-[r:HAS_ENTITIES]->(n2)" % (graph_name, row['Intent'], row['Question'], graph_name, row['Entities'], row['Intent'])
        df.loc[index, 'edge3_query'] = "MATCH (n1:%s:Entities {values:'%s', intent:'%s'}),(n2:%s:Response {content:'%s'}) MERGE (n1)-[r:HAS_RESPONSE]->(n2)" % (graph_name, row['Entities'], row['Intent'], graph_name, row['Answer'])

    for index, row in df.iterrows():
        with driver.session() as session:
            result = session.run(row['question_query'])
            result = session.run(row['intent_query'])
            result = session.run(row['entities_query'])
            result = session.run(row['response_query'])

            result = session.run(row['edge1_query'])
            result = session.run(row['edge2_query'])
            result = session.run(row['edge3_query'])

    a=2
    return a

def extract_utterances(df,graph_name):

    df = df.replace(np.nan, '', regex=True)
    df.replace({r'\A\s+|\s+\Z': '', '\n': ' ', "'": ''}, regex=True, inplace=True)
    df = df.replace('', np.nan)

    df['Utterances'] = df[df.columns[1:]].apply(lambda x: '##'.join(x.dropna().astype(str)), axis=1)

    df = df[['Q Number', 'Question', 'Utterances']]
    df['Utterances'] = df[['Utterances']].values.tolist()
    df['node_query'] = ""
    df['edge_query'] = ""


    for index, row in df.iterrows():
        list = row['Utterances'][0].split("##")
        node_list = []
        edge_list = []
        for item in list:
            if item != '':
                node_query = "MERGE(n2:%s:Utterance {content:'%s',q_id:'%s'})" % (graph_name, item, row['Q Number'])
                edge_query = "MATCH (n1:%s:Question {q_id:'%s'}),(n2:%s:Utterance {content:'%s'}) MERGE (n1)-[r:HAS_UTTERANCE]->(n2)" % (graph_name, row['Q Number'], graph_name, item)
                node_list.append(node_query)
                edge_list.append(edge_query)

        df.at[index, 'node_query'] = node_list
        df.at[index, 'edge_query'] = edge_list

    print('we are here2')


    for index, row in df.iterrows():
        node_list = row['node_query']
        edge_list = row['edge_query']
        for item in node_list:
            # print(item,'\n')
            with driver.session() as session:
                result = session.run(item)
        for item in edge_list:
            # print(item,'\n')
            with driver.session() as session:
                result = session.run(item)

    b=2
    return b

def extract_syns(df,graph_name):
    df = df.replace(np.nan, '', regex=True)
    df.replace({r'\A\s+|\s+\Z': '', '\n': ' ', "'": ''}, regex=True, inplace=True)
    df['Synonyms'] = df[df.columns[1:]].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)

    df = df[['Entity_value', 'Synonyms']]
    df['Synonyms'] = df[['Synonyms']].values.tolist()
    df['node_query'] = ""
    df['edge_query'] = ""

    for index, row in df.iterrows():
        list = row['Synonyms'][0].split(",")
        print(list)
        node_list = []
        edge_list = []
        for item in list:
            node_query = "MERGE(n2:%s:Synonym {key:'%s',value:'%s'})" % (graph_name, row['Entity_value'], item)
            edge_query = "MATCH (n1:%s:Entities {values:'%s'}),(n2:%s:Synonym {value:'%s'}) MERGE (n1)-[r:HAS_SYNONYM]->(n2)" % (graph_name, row['Entity_value'], graph_name, item)
            node_list.append(node_query)
            edge_list.append(edge_query)
        row['node_query'] = node_list
        row['edge_query'] = edge_list

    for index, row in df.iterrows():
        node_list = row['node_query']
        edge_list = row['edge_query']
        for item in node_list:
            # print(item,'\n')
            with driver.session() as session:
                result = session.run(item)
        for item in edge_list:
            # print(item,'\n')
            with driver.session() as session:
                result = session.run(item)

    c=2
    return c