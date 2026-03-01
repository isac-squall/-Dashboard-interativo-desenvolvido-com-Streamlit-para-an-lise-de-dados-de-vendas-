import os

import pandas as pd
import plotly.express as px  # type: ignore
import streamlit as st

st.set_page_config(layout="wide")

# Com uma visão mensal
#faturamento por unidade…
# tipo de produto mais vendido, contribuição por filial,
#Desempenho das forma de pagamento…
#Como estão as avaliações das filiais?

# Sidebar para upload de arquivo
st.sidebar.title("📁 Upload de Arquivo")
uploaded_file = st.sidebar.file_uploader("Envie um arquivo CSV ou XLS", type=["csv", "xls", "xlsx"])

if uploaded_file is not None:
    # Carregar arquivo enviado
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, sep=";", decimal=",")  # type: ignore
    else:
        df = pd.read_excel(uploaded_file)  # type: ignore

    st.sidebar.success(f"✅ Arquivo '{uploaded_file.name}' carregado com sucesso!")
else:
    # Carregar arquivo padrão
    try:
        # Obter o caminho do diretório do script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "supermarket_sales.csv")
        df = pd.read_csv(file_path, sep=";", decimal=",")  # type: ignore
        st.sidebar.info("📊 Usando dados padrão (supermarket_sales.csv)")
    except FileNotFoundError:
        st.error("❌ Arquivo padrão não encontrado. Faça upload de um arquivo para continuar.")
        st.stop()

# Verificar se as colunas necessárias existem
st.write("**Colunas disponíveis:**", df.columns.tolist())

# Tentar encontrar coluna de data com diferentes nomes
date_columns = [col for col in df.columns if col.lower() in ['date', 'data', 'data de compra', 'data da compra']]
if date_columns:
    date_col = date_columns[0]
else:
    date_col = st.sidebar.selectbox("Qual coluna contém a data?", df.columns)

# filtros adicionais: filial / cidade, produto e cliente
string_cols_all = df.select_dtypes(include=['object']).columns.tolist()

# filtro de filial ou cidade
branch_cols = [col for col in string_cols_all if col.lower() in ['city', 'cidade', 'filial', 'branch']]
if branch_cols:
    branch_choice = st.sidebar.multiselect("Filial / Cidade", sorted(df[branch_cols[0]].dropna().unique()))
    if branch_choice:
        df = df[df[branch_cols[0]].isin(branch_choice)]

# filtro de linha/categoria de produto
prod_cat_cols = [col for col in string_cols_all if col.lower() in ['category', 'categoria', 'product line', 'tipo de produto']]
if prod_cat_cols:
    prod_choice = st.sidebar.multiselect("Categoria de produto", sorted(df[prod_cat_cols[0]].dropna().unique()))
    if prod_choice:
        df = df[df[prod_cat_cols[0]].isin(prod_choice)]

# filtros de cliente (tipo, gênero, etc.)
cust_cols = [col for col in string_cols_all if col.lower() in ['customer type', 'tipo de cliente']]
if cust_cols:
    cust_choice = st.sidebar.multiselect("Tipo de cliente", sorted(df[cust_cols[0]].dropna().unique()))
    if cust_choice:
        df = df[df[cust_cols[0]].isin(cust_choice)]

gender_cols = [col for col in string_cols_all if col.lower() in ['gender', 'sexo', 'genero']]
if gender_cols:
    gender_choice = st.sidebar.multiselect("Gênero", sorted(df[gender_cols[0]].dropna().unique()))
    if gender_choice:
        df = df[df[gender_cols[0]].isin(gender_choice)]

# meta de faturamento para comparação
meta_sales = st.sidebar.number_input("Meta de faturamento para o mês (R$)", min_value=0.0, step=100.0, format="%.2f")

# detectar colunas de custo/margem
numeric_cols_all = df.select_dtypes(include=['number']).columns.tolist()
cost_cols = [col for col in numeric_cols_all if 'cost' in col.lower() or 'custo' in col.lower()]
margin_cols = [col for col in numeric_cols_all if 'margin' in col.lower() or 'margem' in col.lower()]

# Converter para datetime
if date_col:
    try:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')  # type: ignore
        df = df.sort_values(date_col)
        df["Month"] = df[date_col].apply(lambda x: str(x.year) + "-" + str(x.month).zfill(2) if pd.notna(x) else "Sem data")  # type: ignore
        month = st.sidebar.selectbox("Mês", df["Month"].unique())
        df_filtered = df[df["Month"] == month]  # type: ignore
    except Exception as e:
        st.error(f"❌ Erro ao processar coluna de data: {e}")
        st.stop()
else:
    st.error("❌ Não foi possível encontrar uma coluna de data no arquivo.")
    st.stop()

# depois do filtro mensal, prepare colunas e identificar tipos
# precisamos saber qual coluna numérica será usada para os cálculos e gráficos
numeric_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()  # type: ignore
string_cols = df_filtered.select_dtypes(include=['object']).columns.tolist()  # type: ignore
# colunas de avaliação frequentemente usadas em gráficos
rating_cols = [col for col in numeric_cols if col.lower() in ['rating', 'avaliação', 'nota']]

val_col = numeric_cols[0] if numeric_cols else None

date_col_available = date_col in df_filtered.columns  # type: ignore

# gráfico de tendência mensal global (antes de filtrar por mês específico)
if date_col_available and val_col:
    try:
        trend = df.groupby("Month")[val_col].sum().reset_index().sort_values("Month")  # type: ignore
        fig_trend = px.line(trend, x="Month", y=val_col, title="Tendência de faturamento por mês")  # type: ignore
        if meta_sales > 0:
            # adicionar linha de meta constante
            trend['Meta'] = meta_sales
            fig_trend.add_scatter(x=trend['Month'], y=trend['Meta'], mode='lines', name='Meta', line={'dash':'dash'})  # type: ignore
        st.subheader("📈 Tendência Mensal")
        st.plotly_chart(fig_trend, width='stretch', key="trend")
    except Exception:
        pass
# - receita total
# - número de transações
# - ticket médio
# - taxa de conversão (pedidos / visitantes)
# - custo de aquisição de cliente (CAC)
# - crescimento mensal (se possível)
# - valor médio por filial ou produto

# calcular métricas básicas
val_col = numeric_cols[0] if numeric_cols else None
if val_col:
    total_sales = df_filtered[val_col].sum()  # type: ignore
    order_count = len(df_filtered)  # type: ignore
    avg_order = total_sales / order_count if order_count else 0  # type: ignore
else:
    total_sales = order_count = avg_order = 0

# taxa de conversão e CAC exigem dados externos; permitimos entrada manual
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧮 Métricas de Vendas Avançadas")
st.sidebar.write("Se você tiver informações sobre visitantes ou custo de aquisição, insira abaixo.")

visitors = st.sidebar.number_input("Número de visitantes no período", min_value=0, step=1, format="%d")
conv_rate = (order_count / visitors * 100) if visitors and order_count else None

cac_cost = st.sidebar.number_input("Custo total de aquisição de clientes (R$)", min_value=0.0, step=1.0, format="%.2f")
cac = (cac_cost / order_count) if order_count and cac_cost else None

# cálculo de crescimento mensal (compara mês anterior)
prev_month = None
if date_col_available:
    # assume Month formato 'YYYY-M'
    months = sorted(df["Month"].dropna().unique())
    if month in months:
        idx = months.index(month)
        if idx > 0:
            prev_month = months[idx - 1]
            prev_sales = df[df["Month"] == prev_month][val_col].sum() if val_col else 0  # type: ignore
            growth = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales else None  # type: ignore
        else:
            growth = None
    else:
        growth = None
else:
    growth = None

# dividir em abas para vendas, clientes e produtos
vendas_tab, clientes_tab, produtos_tab = st.tabs(["Vendas", "Clientes", "Produtos"])

with vendas_tab:
    # mostrar KPIs no topo
    # adicionamos duas colunas extras para taxa de conversão e CAC
    kpicol1, kpicol2, kpicol3, kpicol4, kpicol5 = st.columns(5)
    kpicol1.metric("Receita Total", f"R$ {total_sales:,.2f}")
    kpicol2.metric("Ordens", f"{order_count}")
    kpicol3.metric("Ticket Médio", f"R$ {avg_order:,.2f}")
    if conv_rate is not None:
        kpicol4.metric("Taxa de Conversão", f"{conv_rate:.2f}%")
    else:
        kpicol4.metric("Taxa de Conversão", "N/A")
    if cac is not None:
        kpicol5.metric("CAC (R$)", f"R$ {cac:,.2f}")
    else:
        kpicol5.metric("CAC (R$)", "N/A")

    # crescimento continua abaixo em outras colunas
    kpicol_a, kpicol_b = st.columns(2)
    if growth is not None:
        kpicol_a.metric("Crescimento Mês Anterior", f"{growth:.2f}%")
    else:
        kpicol_a.metric("Crescimento Mês Anterior", "N/A")

    # comparar com meta se fornecida
    if meta_sales > 0:
        diff = total_sales - meta_sales  # type: ignore
        pct = (diff / meta_sales * 100) if meta_sales else 0  # type: ignore
        st.write(f"Meta mensal: R$ {meta_sales:,.2f}")
        st.write(f"Diferença: R$ {diff:,.2f} ({pct:.1f}% {'acima' if diff>=0 else 'abaixo'})")

    # calcular margem/bruto se colunas existirem
    if cost_cols or margin_cols:
        if cost_cols:
            cost_col = cost_cols[0]
            profit = total_sales - df_filtered[cost_col].sum()  # type: ignore
            st.write(f"Lucro bruto estimado (usando {cost_col}): R$ {profit:,.2f}")
            if total_sales:
                st.write(f"Margem bruta: {profit/total_sales*100:.1f}%")
        if margin_cols:
            mar_col = margin_cols[0]
            avg_margin = df_filtered[mar_col].mean()  # type: ignore
            st.write(f"Margem média ({mar_col}): {avg_margin:.1f}%")

    # depois dos KPIs, continuar com layout de gráficos
    col1, col2 = st.columns(2)
    col3, col4, col5 = st.columns(3)

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Personalizar Gráficos")

    # Gráfico 1: Faturamento por dia
    if date_col in df_filtered.columns and numeric_cols:  # type: ignore
        try:
            fig_date = px.bar(df_filtered, x=date_col, y=numeric_cols[0],  # type: ignore
                             title="Faturamento por dia")
            col1.plotly_chart(fig_date, width='stretch', key="date_chart")
        except Exception as e:
            col1.warning(f"Não foi possível criar este gráfico: {e}")
    # identificação da coluna de produto
    prod_cols = [col for col in string_cols if col.lower() in ['product', 'produto', 'item', 'product line']]
    if prod_cols and val_col:
        prod_col = prod_cols[0]
        try:
            top_products = df_filtered.groupby(prod_col)[val_col].sum().nlargest(10).reset_index()  # type: ignore
            fig_top = px.bar(top_products, x=prod_col, y=val_col, title="Top 10 produtos por receita")  # type: ignore
            st.subheader("🔝 Top Produtos")
            st.plotly_chart(fig_top, width='stretch', key="top_products")
        except Exception as e:
            st.warning(f"Não foi possível gerar gráfico de top produtos: {e}")
    if branch_cols and val_col:
        try:
            bc = branch_cols[0]
            avg_by_branch = df_filtered.groupby(bc)[val_col].mean().reset_index()  # type: ignore
            fig_branch = px.bar(avg_by_branch, x=bc, y=val_col, title="Ticket médio por filial/cidade")  # type: ignore
            st.subheader("📍 Ticket médio por filial")
            st.plotly_chart(fig_branch, width='stretch', key="branch_ticket")
        except Exception as e:
            st.warning(f"Não foi possível gerar gráfico de ticket por filial: {e}")
    if rating_cols:
        rt = rating_cols[0]
        try:
            st.subheader("⭐ Estatísticas de Avaliação")
            avg_rating = df_filtered[rt].mean()  # type: ignore
            st.write(f"Avaliação média: {avg_rating:.2f}")
            fig_hist = px.histogram(df_filtered, x=rt, nbins=10, title="Distribuição de avaliações")  # type: ignore
            st.plotly_chart(fig_hist, width='stretch', key="hist_rating")
        except Exception as e:
            st.warning(f"Erro ao analisar avaliações: {e}")

    # tabela de resumo de KPI por filial/categoria
    try:
        summary_cols = []
        if branch_cols:
            summary_cols.append(branch_cols[0])
        if prod_cols:
            summary_cols.append(prod_cols[0])
        if summary_cols and val_col:
            summary = (
                df_filtered.groupby(summary_cols)  # type: ignore
                .agg(Total_Sales=(val_col, 'sum'),
                     Orders=(val_col, 'count'),
                     Avg_Ticket=(val_col, 'mean'))
                .reset_index()  # type: ignore
            )
            st.subheader("📋 Resumo de KPI")
            st.dataframe(summary)  # type: ignore
            # botão para exportar
            csv = summary.to_csv(index=False).encode('utf-8')  # type: ignore
            st.download_button(label="📥 Baixar resumo CSV", data=csv, file_name="resumo_kpi.csv", mime="text/csv")  # type: ignore
            # também oferecer Excel
            try:
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    summary.to_excel(writer, index=False, sheet_name='Resumo')  # type: ignore
                excel_data = output.getvalue()
                st.download_button(
                    label="📥 Baixar resumo XLSX",
                    data=excel_data,
                    file_name="resumo_kpi.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            except Exception as e:
                st.warning(f"Erro ao gerar Excel: {e}")
            # Observação sobre PDF
            st.info(
                "Imprima esta página (Ctrl+P) para gerar PDF ou utilize ferramentas externas, pois exportação direta ainda não está implementada."
            )
    except Exception as e:
        st.warning(f"Não foi possível gerar tabela de resumo: {e}")

    # gráficos adicionais após resumo
    # Gráfico 2: Por categoria
    if string_cols and numeric_cols:
        try:
            cat_col = st.sidebar.selectbox("Coluna de categoria:", string_cols, key="cat1")
            fig_prod = px.bar(df_filtered, x=date_col if date_col in df_filtered.columns else numeric_cols[0],  # type: ignore
                             y=cat_col, title="Distribuição por categoria",
                             orientation="v")
            col2.plotly_chart(fig_prod, width='stretch', key="cat_dist")
        except Exception as e:
            col2.warning(f"Não foi possível criar este gráfico: {e}")

    # Gráfico 3: Por cidade/localidade
    if string_cols and numeric_cols:
        try:
            location_cols = [col for col in string_cols if col.lower() in ['city', 'cidade', 'filial', 'branch']]
            if location_cols:
                location_col = location_cols[0]
            else:
                location_col = st.sidebar.selectbox("Coluna de localidade:", string_cols, key="loc")

            city_total = df_filtered.groupby(location_col)[[numeric_cols[0]]].sum().reset_index()  # type: ignore
            fig_city = px.bar(city_total, x=location_col, y=numeric_cols[0],  # type: ignore
                             title=f"Faturamento por {location_col.lower()}")
            col3.plotly_chart(fig_city, width='stretch', key="city_sales")
        except Exception as e:
            col3.warning(f"Não foi possível criar este gráfico: {e}")

    # Gráfico 4: Por tipo de pagamento
    if string_cols and numeric_cols:
        try:
            payment_cols = [col for col in string_cols if col.lower() in ['payment', 'pagamento', 'forma de pagamento']]  # type: ignore
            if payment_cols:
                payment_col = payment_cols[0]
                fig_kind = px.pie(df_filtered, values=numeric_cols[0], names=payment_col,  # type: ignore
                                title="Faturamento por tipo de pagamento")
                col4.plotly_chart(fig_kind, width='stretch', key="payment_pie")
            else:
                col4.info("Nenhuma coluna de pagamento encontrada")
        except Exception as e:
            col4.warning(f"Não foi possível criar este gráfico: {e}")

    # Gráfico 5: Avaliações
    if string_cols:
        try:
            rating_cols = [col for col in numeric_cols if col.lower() in ['rating', 'avaliação', 'nota']]  # type: ignore
            location_cols = [col for col in string_cols if col.lower() in ['city', 'cidade', 'filial', 'branch']]  # type: ignore

            if rating_cols and location_cols:
                rating_col = rating_cols[0]
                location_col = location_cols[0]
                fig_rating = px.bar(df_filtered, y=rating_col, x=location_col,  # type: ignore
                                   title="Avaliação por localidade")
                col5.plotly_chart(fig_rating, width='stretch', key="rating_by_loc")
            else:
                col5.info("Nenhuma coluna de avaliação encontrada")
        except Exception as e:
            col5.warning(f"Não foi possível criar este gráfico: {e}")

# conteúdo para as abas de clientes e produtos

with clientes_tab:
    st.subheader("🔍 Análise de Clientes")
    # contagens por tipo de cliente
    if cust_cols:
        cust_col = cust_cols[0]
        cust_summary = df_filtered[cust_col].value_counts().reset_index()  # type: ignore
        cust_summary.columns = [cust_col, 'Count']
        fig_cust = px.bar(cust_summary, x=cust_col, y='Count',  # type: ignore
                          title="Quantidade por tipo de cliente")
        st.plotly_chart(fig_cust, width='stretch', key="cust_bar")
        # ticket médio por tipo de cliente
        if val_col:
            avg_by_cust = df_filtered.groupby(cust_col)[val_col].mean().reset_index()  # type: ignore
            avg_by_cust = avg_by_cust.rename(columns={val_col: 'Avg_Ticket'})  # type: ignore
            st.dataframe(avg_by_cust)  # type: ignore
    if gender_cols:
        gen_col = gender_cols[0]
        gen_summary = df_filtered[gen_col].value_counts().reset_index()  # type: ignore
        gen_summary.columns = [gen_col, 'Count']
        fig_gen = px.pie(gen_summary, names=gen_col, values='Count',  # type: ignore
                         title="Distribuição por gênero")
        st.plotly_chart(fig_gen, width='stretch', key="gender_pie")

with produtos_tab:
    st.subheader("📦 Análise de Produtos")
    # faturamento por categoria de produto
    if prod_cat_cols:
        cat_col = prod_cat_cols[0]
        if val_col:
            cat_sales = df_filtered.groupby(cat_col)[val_col].sum().reset_index()  # type: ignore
            fig_cat = px.bar(cat_sales, x=cat_col, y=val_col,  # type: ignore
                             title="Faturamento por categoria de produto")
            st.plotly_chart(fig_cat, width='stretch', key="cat_sales")
    # top produtos
    prod_cols = [col for col in string_cols if col.lower() in ['product', 'produto', 'item', 'product line']]  # type: ignore
    if prod_cols and val_col:
        prod_col = prod_cols[0]
        top_products = df_filtered.groupby(prod_col)[val_col].sum().nlargest(10).reset_index()  # type: ignore
        fig_top2 = px.bar(top_products, x=prod_col, y=val_col,  # type: ignore
                          title="Top 10 produtos por receita")
        st.plotly_chart(fig_top2, width='stretch', key="top_products_tab")
