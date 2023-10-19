import pandas as pd
from datetime import datetime
import warnings
# Desabilitar warnings do pandas
warnings.filterwarnings( 'ignore' )
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None) 



def check_loan_inputs(rate, loan, term, carencia):
    errors = []

    if rate <= 0:
        errors.append("A taxa de juros deve ser maior que zero.")
    if loan <= 0:
        errors.append("O valor do empréstimo deve ser maior que zero.")
    if term <= 0:
        errors.append("O prazo do empréstimo deve ser maior que zero.")
    if carencia < 0 or carencia >= term:
        errors.append("O período de carência não pode ser negativo e nem maior que o prazo.")

    return errors



# INPUTS PARA CALCULO DA AMORTIZACAO
def inputs(rate, loan, term, carencia, start_date):
            
            errors = check_loan_inputs(rate, loan, term, carencia)

            if errors: return errors 


            rate_day = (rate + 1) ** (1 / 30) - 1

            if carencia == 0:ajust_loan = loan
            elif carencia < 1: ajust_loan = loan - ((rate_day + 1) ** (30 - carencia * 30) - 1) * loan
            else: ajust_loan = ((rate_day + 1) ** (carencia * 30) - 1) * loan + loan
            pmt = ajust_loan * (rate * (1 + rate) ** (term - carencia)) / ((1 + rate) ** (term - carencia) - 1)

            new_data = {'rate': rate, 'rate_day': rate_day, 'carencia': carencia, 'ajust_loan': ajust_loan, 'loan': loan, 'term': term, 'pmt': pmt, 'startDate': start_date}

            df_loan = pd.DataFrame(new_data, index=[0])

            return df_loan



# FUNCAO CALCULA CURVA DO CONTRATO
def amort_by_column(df):
    max_term = int(df['term'].max())

    for i in range(max_term+1):
        df[f'startDate_{i}'] = df['startDate'] + pd.DateOffset(months=i)
        df[f'pagtoDate_{i}'] = df[f'startDate_{i}']

        if i == 0:
            df[f'EA_{i}'] = df['loan']
            df[f'prestacao_{i}'] = 0
            df[f'amortizacao_{i}'] = 0
            df[f'juros_{i}'] = 0

        else:
            # Se tiver em período de carência:
            df['mob'] = i
            for index, row in df.iterrows():
                if i <= row['carencia']:
                    df.at[index, f'prestacao_{i}'] = 0
                    df.at[index, f'amortizacao_{i}'] = 0
                    df.at[index, f'juros_{i}'] = row[f'EA_{i-1}'] * row['rate']
                    df.at[index, f'EA_{i}'] = row[f'EA_{i-1}'] + df.at[index, f'juros_{i}']

                else:
                    if i == 1:
                        amortization_value = (row['pmt'] - round(((row['rate_day'] + 1) ** 30 - 1) * row[f'EA_{i-1}'], 4))
                    else:
                        amortization_value = (row['pmt'] - round(row[f'EA_{i-1}'] * row['rate'], 4))

                    df.at[index, f'amortizacao_{i}'] = amortization_value if i <= row['term'] else 0

                    days = (row[f'startDate_{i}'].day - row[f'pagtoDate_{i}'].day)
                    df.at[index, f'prestacao_{i}'] = (row['pmt'] / round((row['rate_day'] ** days), 4)) if i <= row['term'] else 0
                    df.at[index, f'juros_{i}'] = df.at[index, f'prestacao_{i}'] - df.at[index, f'amortizacao_{i}']
                    df.at[index, f'EA_{i}'] = df.at[index, f'EA_{i-1}'] - df.at[index, f'amortizacao_{i}']

                if i == row['term']: df.at[index, f'EA_{i}'] = round( df.at[index,f'EA_{i}'])
                elif  i > row['term']: df.at[index, f'EA_{i}'] = 0

    return df



# FUNCAO PARA TRATAMENTO DOS DADOS E VERTICALIZANDO A TABELA
def processar_dataframe(df):
    prefixos = [item.split('0')[0] for item in df.filter(like='_0').columns]

    for i, prefix in enumerate(prefixos):
        if i == 0:
            new_df = df.filter(like=prefix).T
            column = new_df.iloc[0].T.name
            column = column.split('_')[0]
            new_df = new_df.rename(columns={0: column})
            new_df['fk'] = new_df.index
            new_df['fk'] = new_df['fk'].apply(lambda x: x.split('_')[-1]).astype(int)
            new_df.set_index('fk')
        else:
            df_2 = df.filter(like=prefix).T
            column = df_2.iloc[0].T.name
            column = column.split('_')[0]
            df_2 = df_2.rename(columns={0: column})
            df_2['fk'] = df_2.index
            df_2['fk'] = df_2['fk'].apply(lambda x: x.split('_')[-1]).astype(int)
            df_2.set_index('fk')

            new_df[column] = df_2[[column]].values

    ordem_desejada = ['fk', 'startDate', 'pagtoDate', 'prestacao', 'amortizacao', 'juros', 'EA']
    new_df = new_df[ordem_desejada]
    new_df = new_df.set_index('fk')

    return new_df