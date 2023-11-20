import pandas as pd
from datetime import datetime
from dash import dash_table
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output  
import plotly.express as px
import plotly.graph_objects as go  
import dash_bootstrap_components as dbc
import dash_auth

#read the data 
customer_purchase = pd.read_csv('https://github.com/nourhan-waleeed/Elrehab_data/raw/main/customer_purchase.zip')
points_trans = pd.read_csv('https://github.com/nourhan-waleeed/Elrehab_data/raw/main/points_trans.zip')
complaints = pd.read_csv('https://github.com/nourhan-waleeed/Elrehab_data/raw/main/complaints.zip')
complaints_info = pd.read_csv('https://github.com/nourhan-waleeed/Elrehab_data/raw/main/complaints_info.zip')
butchery = pd.read_csv('https://github.com/nourhan-waleeed/Elrehab_data/raw/main/elrehab_survey_butchery.zip')
delivery = pd.read_csv('https://github.com/nourhan-waleeed/Elrehab_data/raw/main/elrehab_survey_delivery.zip')
fish = pd.read_csv('https://github.com/nourhan-waleeed/Elrehab_data/raw/main/elrehab_survey_fish.zip')
point = pd.read_csv('https://github.com/nourhan-waleeed/Elrehab_data/raw/main/elrehab_survey_points.zip')

#customer who already left 
left_customers = complaints_info[complaints_info['complaint_in_days']<= complaints_info['recency_in_days']]
left_customers = left_customers[left_customers['complaint_count']>1]


# the time in days in which the customer was comming regulary
customer_purchase['duration'] = customer_purchase['tenure']- customer_purchase['recency_in_days']
#one visit segment -> the customer who came once {in which month}
one_visit_data = customer_purchase[customer_purchase['segments'] == 'One Visit']
monthly_purchases = one_visit_data.groupby('الشهر ')['segments'].count().reset_index()

# drop down + plot each complaint department and reason
dep = complaints.groupby(['Department','reason']).size().reset_index(name='count')
#groupby each segment
seg = customer_purchase.groupby('segments').size().reset_index(name='count')

#line of the sales of each category in each month
sales = customer_purchase.groupby(['الشهر ','القسم السلعي'])['المشتريات'].sum().reset_index()

#radio item {the first plots}
daily_payments = points_trans.groupby('اسم اليوم')['قيمه المشتريات'].sum().reset_index()
monthly_payments = points_trans.groupby('الشهر')['قيمه المشتريات'].sum().reset_index()
seasonality_payments = points_trans.groupby('فصول')['قيمه المشتريات'].sum().reset_index()

#group by segments
unique_segments = customer_purchase.groupby("رقم العميل")["segments"].unique().reset_index()
segment_counts = unique_segments['segments'].value_counts().reset_index()
segment_counts = segment_counts.rename(columns={'segments': 'Segment', 'index': 'count'})

#drop down options
category_dropdown_options = [{'label': customer_purchase, 'value': customer_purchase} for customer_purchase in customer_purchase['القسم السلعي'].unique()]
segments_dropdown_options = [{'label': segment, 'value': segment} for segment in seg['segments'].unique()]
comp_dropdown_options = [{'label': department, 'value': department} for department in dep['Department'].unique()]

#purchases of each segment 
merged_other = customer_purchase[customer_purchase['segments'].isin(['Champion', 'Need Attention','One Visit'])]
merged_loyal = customer_purchase[customer_purchase['segments']=='Loyal']
# groupby segment and each category
other_counts = merged_other.groupby(['segments', 'القسم السلعي']).size().reset_index(name='count')
loyal_counts = merged_loyal.groupby(['segments', 'القسم السلعي']).size().reset_index(name='count')

#category part:

#SUM sales from each category 
category_sum = customer_purchase.groupby('القسم السلعي')['المشتريات'].sum().reset_index()
#COUNT sales from each category 
category_count = customer_purchase.groupby('القسم السلعي')['المشتريات'].count().reset_index()
category_sum=category_sum.rename(columns={'المشتريات': 'قيمة المشتريات'})
category_count=category_count.rename(columns={'المشتريات': 'عدد المنتجات'})
category_merge=pd.merge(category_sum, category_count, on='القسم السلعي', how='inner')

# number of visits plot
no_visits= points_trans.groupby('عدد الزيارات')['رقم العميل'].count().reset_index()

no_methods= complaints.groupby('Method of solution')['Ticket No'].count().reset_index()
no_source= complaints.groupby('Source')['Ticket No'].count().reset_index()

comp_bar = complaints_info.groupby('segments')['Ticket No'].count().reset_index()

customer_reason_counts = left_customers.groupby(['Ticket No', 'reason']).size().reset_index(name='count')

c= complaints_info[['Ticket No','segments','leave_or_stay']]

#for line plot complaint date
complaints_info['complaint date'] = pd.to_datetime(complaints_info['complaint date']).dt.date
complaints_info['complaint date'] = complaints_info['complaint date'].apply(lambda x: x.strftime('%Y-%m-%d'))
date = complaints_info.groupby('complaint date').size().reset_index(name='count')

c = c.drop_duplicates()
#bar to visualize the number of STAYED AND LEFT customers
c =c.groupby('leave_or_stay')[['Ticket No']].count().reset_index()

#repeated complaints by each cutomer {customers who have done more than one complaint}
customer_counts = complaints_info['Ticket No'].value_counts()
repeated_customers = customer_counts[customer_counts > 1].index
repeated_customer_records = complaints_info[complaints_info['Ticket No'].isin(repeated_customers)]

# 8 of the 99 didn't come after the complaints
a = repeated_customer_records[repeated_customer_records['complaint_in_days']<= repeated_customer_records['recency_in_days']]

#table to show the people who didn't come agian
a = a[['Customoer ID','Department','reason','Satisfaction','Visits_No','segments','complaint_count','complaint_in_days','recency_in_days']]


##DELIEVERY
mean_d = {
    'Mean': [4.792683, 4.484053, 4.724203, 4.813321],
    'Category': ['الالتزام الطيار بالاجراءات الاحترازيه', 'مده وصول الاوردر', 'توافر اصناف', 'مستوي خدمه متلقي الاوردر']
}
mean_d = pd.DataFrame(mean_d)
mean_d.columns = ['Mean', 'Category']
overall_mean_d = mean_d['Mean'].mean()
delivery['نوع المكالمة']=delivery['نوع المكالمة'].replace('شكر ', 'شكر')
grouped_delivery = delivery.groupby('نوع المكالمة').size().reset_index(name='count')
grouped_delivery


##FISH
mean_f =  {
    'Mean': [4.691776, 4.887009, 4.861998, 4.663528, 4.722966],
    'Category': ['جوده المنتج - التغليف', 'خدمه متلقي الاوردر', 'وصول الاوردر بالميعاد المحدد', 'الخدمه مرضيه بشكل عام', 'ارتداء الطيار الكمامة']
}
mean_f = pd.DataFrame(mean_f)
mean_f.columns = ['Mean', 'Category']
overall_mean_f = mean_f['Mean'].mean()
grouped_fish = fish.groupby('نوع المكالمة').size().reset_index(name='count')
grouped_fish


##POINTS
mean_p =  {
    'Mean': [4.955774, 4.959869, 4.921376, 4.938575, 4.957412],
    'Category': [
        'مدى الالتزام الفرع بالاجراءات الاحترازية',
        'مدي رضاء العميل عن نظافة المكان',
        'مدي رضاء العميل عن معاملة العاملين بالفرع',
        'مدي رضاء العميل عن اسعار المنتجات داخل الفرع',
        'مدي رضاء العميل عن تنوع المنتجات'
    ]
}

mean_p = pd.DataFrame(mean_p)
mean_p.columns = ['Mean', 'Category']
overall_mean_p = mean_p['Mean'].mean()
point['نوع المكالمة']=point['نوع المكالمة'].replace('شكر ', 'شكر')
point['نوع المكالمة']=point['نوع المكالمة'].replace('اقتراح ', 'اقتراح')

grouped_point = point.groupby('نوع المكالمة').size().reset_index(name='count')
grouped_point


##BUTCHERY
x = ['هل انت راض عن جودة اللحوم المقدمه داخل القسم', 'هل انت راض عن مذاق اللحوم الموجوده بالقسم', 'هل انت راض عن مستوى جودة الخدمه بشكل عام', 'هل انت راض عن وقت التسويه للحوم المباعه بالقسم']
data_yes = [7437, 7538, 6858, 7539]
data_no = [551, 450, 1130, 449]
df= pd.DataFrame({
    'Question': x,
    'Yes': data_yes,
    'No': data_no
})
df['Response']= ['Yes', 'No'] * (len(df)//2)

butchery['نوع الاستبيان']=butchery['نوع الاستبيان'].replace('شكر ', 'شكر')
grouped_butchery = butchery.groupby('نوع الاستبيان').size().reset_index(name='count')
grouped_butchery



# selected features to be shown as a default in drop down list
default=['مخبوزات', 'خضار وفاكهة', 'منظفات', 'تجميل', 'مستلزمات اطفال']

#style
custom_style = {
    'color': 'black',
    'font-family': 'Arial, sans-serif',
    'font-size': '20px'

}

#common style for all the dashboards
common_layout = {
    'plot_bgcolor': '#F6F4EB',
    'paper_bgcolor': '#F6F4EB',
    'font': {
        'color': 'black',
        'size': 15
    },
    'xaxis': {
        'title': {
            #'text': 'X-Axis Label',
            'font': {
                'color': 'black',  # Set the x-axis label color
                'size': 16  # Set the x-axis label font size
            }
        },
        'tickfont': {
            'color': 'black',
            'size': 15
        }
    },
    'yaxis': {
        'title': {
            #'text': 'Y-Axis Label',
            'font': {
                'color': 'black',  # Set the y-axis label color
                'size': 16  # Set the y-axis label font size
            }
        },
        'tickfont': {
            'color': 'black',
            'size': 14
        }
    }
}
# dashboard authentication to open with specific username and password
VALID_USERNAME_PASSWORD_PAIRS = {
    'mohamed_alaa': '1234'
}










app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

custom_color_palette = ['#682C0E', '#C24914', '#BCA37F', '#FC8621', '#346751','#243763']


app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px','background-color': 'white', 'text-align': 'right', 'color': 'black', 'font-size': '22px','mergin-left':'20px','margin-right': '20px'}, children=[
    html.Div([
        html.Img(src=('/assets/img2.png')),
        html.H2(children=' 30/9/2023 فتح الله فرع الرحاب من 1/1/2023 الي  ' ,style={'font-weight': 'bold','text-align': 'right', 'color':'black','background-color': '#FF6000'})
    ],className="banner"),
    html.Hr(style={'border-top': '2px solid #999'}),
    dcc.RadioItems(
        options=[
            {'label': 'نسبة المبيعات على مدار فصول السنة', 'value': 'season'},
            {'label': 'نسبة المبيعات على مدار الاسبوع', 'value': 'days'},
            {'label': 'نسبة المبيعات على مدار الشهر', 'value': 'month'},
            {'label': 'عدد الزيارات ', 'value': 'freq'},
            {'label': 'معدل الشراء', 'value': 'معدل'}

        ],
        value='month',
        id='controls-and-radio-item',
        labelStyle={'display': 'block', 'margin-bottom': '10px', 'font-weight': 'bold', 'color': 'black'}
     ),
    
    html.Div([
        dcc.Graph(
            figure={},
            id='controls-and-graph',
            style={'display': 'inline-block', 'margin-right': '15px', 'border': '2px solid #ddd','border-radius': '10px'}
        ),

        dcc.Graph(
            figure=px.bar(
                monthly_purchases,
                y='segments',
                x='الشهر ',
                color_discrete_sequence=['#FF6000'],
                labels={'segments':'فئات العملاء'
                }
            ).update_layout(
                title='زيارات العملاء من فئه الزياره الواحده(One Visit Segment) ', **common_layout
            ),
            style={'display': 'inline-block', 'margin-left': '15px', 'border': '2px solid #ddd','border-radius': '10px'}
        )
    ], style={'margin-bottom': '20px','display': 'flex', 'margin-bottom': '20px'}),

    html.Div([
        dcc.Graph(
            figure=px.scatter(
                customer_purchase,
                x='recency_in_days',
                y='tenure',
                color='segments',
                labels={
                    "recency_in_days":  ' عدد الايام من اخر عمليه شراء',
                    "tenure": "عدد الايام من اول زياره"
                },
                color_discrete_sequence=['#ED7D31', '#BCA37F', '#6C5F5B', 'orange']
            ).update_layout(
                title='العلاقه بين عدد الايام بعد اخر عمليه شراء مع عدد الايام من اول زياره للعميل لكل فئه ',**common_layout
            ),
            style={'border': '2px solid #ddd','border-radius': '10px'}
        )
    ], style={'margin-bottom': '20px'}),


    
    
    
    
        html.Div([
            dcc.Dropdown(
        id='segment-dropdown',
        options=segments_dropdown_options,
        multi=True,  # Allow for selecting multiple segments
        value=customer_purchase['segments'].unique(),  # Default to all segments
        placeholder="Select segment(s)",
     style={'backgroundColor': '#F6F4EB', 'color': 'black'} 
    ),
            
        dcc.Graph(
                 id='segment-plot',
                 config={'displayModeBar': False},style={'border': '2px solid #ddd','margin-bottom':'10px','margin-top':'10px','border-radius': '10px'}
                  
                  ),
  
            
        ],style={'margin-left':'20px'}),
    
        dash_table.DataTable(
        style_cell=dict(textAlign='right',color='black'),
        style_header=dict(backgroundColor="#FF9130",color ='black'),
        style_data=dict(backgroundColor="#F6F4EB"),    
        id='segment-table',
        columns=[
            {'name': 'رقم العميل', 'id': 'رقم العميل'},
            {'name': 'عدد الزيارات', 'id': 'عدد الزيارات'},
            {'name': 'معدل الشراء', 'id': 'معدل الشراء'},
        ],
        data=[],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#F6F4EB',
            'color': 'black'  # You may need to set text color to ensure readability
        },
        {
            'if': {'row_index': 'even'},
            'backgroundColor': 'white',
            'color': 'black'
        }
    ],
    ),
        html.Div([
            dcc.Dropdown(
        id='category-dropdown',
        options=category_dropdown_options,
        multi=True,  # Allow for selecting multiple segments
        value= default,
        placeholder="Select Category",
        style={'backgroundColor': '#F6F4EB','color':'black','margin-top':'20px'} 
    ),
    
        ],style={'margin-bottom': '5px','margin-left':'20px'}),
    
html.Div([
    dcc.Graph(id='cat-plot1', style={'display': 'inline-block', 'margin-left': '20px','border': '2px solid #ddd','border-radius': '10px'}),
    dcc.Graph(id='cat-plot2', style={'display': 'inline-block', 'margin-left': '20px','border': '2px solid #ddd','border-radius': '10px'}),  # Adjust margin as needed
],style={'display': 'flex', 'margin-bottom': '20px'}),

html.Div([
    dcc.Graph(id='cat-plot3', style={'display': 'inline-block', 'margin-left': '20px','border': '2px solid #ddd','border-radius': '10px'}),
    dcc.Graph(id='cat-plot4', style={'display': 'inline-block', 'margin-left': '20px','border': '2px solid #ddd','border-radius': '10px'}),  # Adjust margin as needed
], style={'display': 'flex', 'margin-bottom': '20px'}),


        
    

        html.Div([

     dcc.Graph(
    figure = px.scatter(customer_purchase, x='duration', y='عدد الزيارات', title='العلاقه بين فتره زياره العميل و عدد الزيارات',size='معدل الشراء',color_discrete_sequence=['#FF6000']
).update_layout(
    xaxis_title='فتره زياره العميل',
    yaxis_title='عدد الزيارات',
    showlegend=False , **common_layout),style={'border': '2px solid #ddd','border-radius': '10px'} )

    ],style={'margin-top': '10px', 'margin-left':'30px'}),
    
    html.Div([
            html.Hr(style={'border-top': '3px solid #999'}),
            html.H1(children='شكاوي فرع الرحاب من 1/1/2023 الي  30/9/2023 ' ,
                     style={'color': '#333', 'font-weight': 'bold','text-align': 'center','color':'black','font-size':'30px'}
                    ),       
    ],className='banner2'),
    
    
            html.Div([
            dcc.Dropdown(
        id='comp-dropdown',
        options=comp_dropdown_options,
        multi=True,  # Allow for selecting multiple segments
        value=dep['Department'].unique(),  # Default to all segments
        placeholder="Select department(s)",
        style={'backgroundColor': '#F6F4EB','color':'black','margin-top':'20px','margin-bottom':'5px'} 
        ,className='black-text-dropdown' 
    ),
            
        dcc.Graph(id='comp-plot',style={'margin-left':'20px','border': '2px solid #ddd','margin-bottom':'20px','margin-top':'5px','border-radius': '10px'}),
  
            
        ],style={'margin-left':'20px'}),
    
    
    html.Div([
        dcc.RadioItems(
        options=[
            {'label': 'طريقة استقبال الشكاوي', 'value': 'Source'},
            {'label': 'طريقة حل الشكاوي', 'value': 'Method Of Solution'}

        ],
        value='Source',
        id='comp-big-radio-item',
        labelStyle={'display': 'block', 'margin-bottom': '17px', 'font-weight': 'bold', 'color': 'black','font-size':'25px'})
    
    
    ]),
    
    
    
    
html.Div([
    dcc.Graph(figure={}, id='source-sol-plot', style={'display': 'inline-block','border': '2px solid #ddd','border-radius': '10px'}),
    dcc.Graph(
        figure=px.bar(
            c,
            x='leave_or_stay',
            y='Ticket No',
            color_discrete_sequence=['#FF6000'],
            title='نسبة المغادرة بمعدل الشكاوي',
        ).update_layout(
            xaxis_title='STAYED                                   LEFT',
            showlegend=False,
            **common_layout
        ),
        style={'display': 'inline-block', 'margin-left': '20px','border': '2px solid #ddd','border-radius': '10px'}  # Adjust margin as needed
    )
], style={'display': 'flex', 'margin-bottom': '20px'}),
  
    
   html.Div([
       dcc.Graph(figure=px.line(
       date,
       x='complaint date',
       y='count',
       color_discrete_sequence=['#FF6000'],
        title='عدد شكاوي فرع الرحاب في الفتره من 1/1/2023 الي 30/9/2023',
        labels={'complaint date': 'تاريخ الشكوى', 'count': 'عدد الشكاوى '}
        ).update_layout(**common_layout),style={'border': '2px solid #ddd','margin-bottom':'20px','border-radius': '10px'})
       ]
       ,style={'display': 'flex', 'flex-direction': 'column','margin-left':'40px'}
),  

        

 
            html.Div([
    dash_table.DataTable(
        data=customer_reason_counts.to_dict('records'),
        columns=[{"name": i, "id": i} for i in customer_reason_counts.columns],
        sort_action='native',
        sort_mode='single',
        style_cell=dict(textAlign='left',color='black'),
        style_header=dict(backgroundColor="#FF9130",color='black'),
        style_data=dict(backgroundColor="#F6F4EB"),
        style_data_conditional=[
            {
                'if': {'filter_query': '{Ticket No} = 608494.0'},
                'backgroundColor': '#F15A59'  # You can assign a unique color for each customer ID here
            },
            {
                'if': {'filter_query': '{Ticket No} = 2'},
                'backgroundColor': 'blue'
            },

    
    
])            
],style={'margin-bottom':'20px'}),   


    
    
html.Div([
    dash_table.DataTable(
        data=a.to_dict('records'),
        columns=[{"name": i, "id": i} for i in a.columns],
        sort_action='native',
        sort_mode='single',
        style_cell=dict(textAlign='left',color='black'),
        style_header=dict(backgroundColor="#FF9130",color ='black'),
        style_data=dict(backgroundColor="#F6F4EB"),
        sort_by=[{'column_id': 'complaint_count', 'direction': 'desc'}]
    ), 
  
]),  
    
    
    



html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='جزاره بلدي الرحاب',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style={'backgroundColor': '#F6F4EB','color':'black','font-weight':'bold'}
            ),
            dcc.Tab(
                label='اسماك الرحاب',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style={'backgroundColor': '#F6F4EB','color':'black','font-weight':'bold'}
            ),
            dcc.Tab(
                label='نقاط الرحاب',
                value='tab-3', className='custom-tab',
                selected_className='custom-tab--selected',
                style={'backgroundColor': '#F6F4EB','color':'black','font-weight':'bold'}
            ),
            dcc.Tab(
                label='توصيل الرحاب',
                value='tab-4',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style={'backgroundColor': '#F6F4EB','color':'black','font-weight':'bold'}
            ),
        ]),
    html.Div(id='tabs-content-classes')
],style={'margin-top':'20px'}),

    
    


    
    
    
    
    
])


@app.callback(
    Output('tabs-content-classes', 'children'),
    Input('tabs-with-classes', 'value')
)


def render_content(tab):
    if tab == 'tab-1':
        return html.Div([

        dcc.Graph(
            figure=px.bar(
                df,
                x='Question',
                y=['Yes', 'No'],
                labels={'y': 'عدد', 'Question':'اسئله استبيان'},
                title='استبيان جزاره فرع الرحاب',
                color_discrete_map={'Yes': '#FF6000', 'No': '#4F200D'}
            ).update_layout(barmode='group', **common_layout),style={'border': '2px solid #ddd','margin-top':'20px','border-radius': '10px'}
            
        ),
            dcc.Graph(
        figure=go.Figure(
            go.Funnel(
                y=grouped_butchery['نوع الاستبيان'],
                x=grouped_butchery['count'],
                marker=dict(color='#FF6000')

            )
        ).update_layout(**common_layout,title=' انواع استبيان جزاره فرع الرحاب '),style={'margin-top':'20px','border-radius': '10px','border': '2px solid #ddd'}
    )
    ])



    elif tab == 'tab-2':
        return html.Div([
            
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("متوسط رضا العملاء علي الاسماك", className="card-title", style={'font-weight': 'bold'}),
                        html.P(f"{overall_mean_f:.2f}", className="card-text", style={'font-weight': 'bold'})
                    ]),
                    style={
                        'width': '20rem',
                        'border-width': '2px',
                        'border-style': 'solid',
                        'box-shadow': '5px 5px 5px #888888',
                        'margin-top': '10px',
                        'margin-right':'100px',
                        'margin-down': '10px',
                        'border': '2px solid #ddd',
                        'backgroundColor': '#F6F4EB'
                    }
                ),
                width={'size': 6, 'offset': 5}
            ),

        ]),

        dcc.Graph(figure=px.line(mean_f, x='Category', y='Mean', title='متوسط رضا العملاء في استبيان اسماك الرحاب',
                                  labels={'Mean': 'المتوسط', 'Category':'اسئله الاستبيان'},color_discrete_sequence=['#FF6000']).update_layout(**common_layout),style={'margin-top':'20px','border': '2px solid #ddd','border-radius': '10px'}),
            
    
            dcc.Graph(
            figure=go.Figure(
            go.Funnel(
            y=grouped_fish['نوع المكالمة'],
            x=grouped_fish['count'],
            marker=dict(color='#FF6000'),
            

        )
    ).update_layout(**common_layout,title=' انواع استبيان اسماك فرع الرحاب '),style={'width': '100%', 'height': '100%', 'border': '2px solid #ddd','margin-top':'20px','border-radius': '10px'}
)
           
        ])


    
    elif tab == 'tab-3':
        return html.Div([
                        
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H4("متوسط رضا العملاء علي برنامج النقاط", className="card-title",style={'font-weight': 'bold'}),
                    html.P(f"{overall_mean_p:.2f}", className="card-text",style={'font-weight': 'bold'})
                ]),
                style={
                    'width': '25rem', 
                    'border-width': '2px',  # Set the border width
                    'border-style': 'solid',  # Set the border style to solid
                    'box-shadow': '5px 5px 5px #888888',
                    'margin-top': '10px',
                    'margin-right':'100px',
                    'margin-down': '20px',
                    'border': '2px solid #ddd'
                     ,'backgroundColor': '#F6F4EB' }    ),
            width={'size': 5, 'offset': 5},  # Center the card within a 12-column layout
        ),
    ),
           dcc.Graph(figure=px.line
             (mean_p, x='Category', y='Mean', title='متوسط رضا العملاء علي برنامج النقاط', labels={'Mean': 'المتوسط','Category':'اسئله برنامج النقاط'},color_discrete_sequence=['#FF6000']).update_layout(**common_layout),style={'border': '2px solid #ddd','margin-top':'20px','border-radius': '10px'}),
            
            dcc.Graph(
        figure=go.Figure(
            go.Funnel(
                y=grouped_point['نوع المكالمة'],
                x=grouped_point['count'],
                marker=dict(color='#FF6000'),
                        )
        ).update_layout(**common_layout,title=' انواع استبيان برنامج النقاط في فرع الرحاب ' ),style={ 'border': '2px solid #ddd','margin-top':'20px','border-radius': '10px'}
    )
        ])
    
    
    elif tab == 'tab-4':
        return html.Div([
            
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H4("متوسط رضا العملاء علي التوصيل", className="card-title",style={'font-weight': 'bold'}),
                    html.P(f"{overall_mean_d:.2f}", className="card-text",style={'font-weight': 'bold'})
                ]),
                style={
                    'width': '20rem', 
                    'border-width': '2px',  # Set the border width
                    'border-style': 'solid',  # Set the border style to solid
                    'box-shadow': '5px 5px 5px #888888',
                    'margin-top': '20px',
                    'margin-bottom':'20px',
                    'margin-right':'100px',
                    'border': '2px solid #ddd'
                    ,'backgroundColor': '#F6F4EB'

                }            ),
                width={'size': 6, 'offset': 5}
        ),
    ),
           dcc.Graph(figure=px.line
             (mean_d, x='Category', y='Mean', title="متوسط رضا العملاء علي التوصيل", labels={'Mean': 'المتوسط','Category':'اسئله التوصيل'},color_discrete_sequence=['#FF6000']).update_layout(**common_layout),style={'border': '2px solid #ddd','border-radius': '10px'}),

            dcc.Graph(
        figure=go.Figure(
            go.Funnel(
                y=grouped_delivery['نوع المكالمة'],
                x=grouped_delivery['count'],
                marker=dict(color='#FF6000')

            )
        ).update_layout(**common_layout, title=' انواع استبيان توصيل فرع الرحاب '),style={'margin-top':'20px','border': '2px solid #ddd','border-radius': '10px'}
    )
            
        ])
    
    
    
@app.callback(
    Output(component_id='source-sol-plot', component_property='figure'),
    Input(component_id='comp-big-radio-item', component_property='value')
)



def update_graph_source_sol(chosen_option):
    if chosen_option == 'Method Of Solution':
        figure = px.bar(
            no_methods,
            y='Method of solution',
            x='Ticket No',
            labels={'Ticket No':'عدد العملاء','Method of solution':'طريقة حل الشكوى'},
            orientation = 'h',
          title='طريقة حل الشكاوي'
            ,color_discrete_sequence=['#FF6000']
        ).update_layout(**common_layout)
        
    else:
        figure = px.bar(
            no_source,
            x='Ticket No' ,
            y='Source',
            labels={'Ticket No':'عدد العملاء','Source':'طريقة استقبال الشكوى'},
            orientation = 'h',
            title='طريقة استقبال الشكاوي'
            ,color_discrete_sequence=['#FF6000']
        ).update_layout(**common_layout)



    return figure










@app.callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(chosen_option):


    
    if chosen_option == 'season':
        figure = px.bar(
            seasonality_payments,
            x='فصول',
            y='قيمه المشتريات',
            title='المبيعات على مدار فصول السنة',
            color_discrete_sequence=['#FF6000']
        ).update_layout(**common_layout)
        
        
    elif chosen_option == 'days':
        figure = px.bar(
            daily_payments,
            x='اسم اليوم',
            y='قيمه المشتريات',
            title='المبيعات على مدار الاسبوع',
            color_discrete_sequence=['#FF6000']
        ).update_layout(**common_layout)

    elif chosen_option == 'month':
        figure = px.line(
            monthly_payments,
            x='الشهر',
            y='قيمه المشتريات',
            title='المبيعات على مدار الشهر',
            color_discrete_sequence=['#FF6000']
        ).update_layout(**common_layout)

    elif chosen_option == 'freq':
        figure = px.histogram(
            points_trans,
            x='عدد الزيارات',
            title='عدد الزيارات',
            color_discrete_sequence=['#FF6000']
        ).update_layout(**common_layout)

    elif chosen_option == 'معدل':
        figure = px.box(
            customer_purchase,
            x='معدل الشراء',
            title='معدل الشراء',
            color_discrete_sequence=['#FF6000']
        ).update_layout(**common_layout)

    return figure







@app.callback(
    Output('segment-plot', 'figure'),
    Input('segment-dropdown', 'value')
)
def update_segment_plot(selected_segments):


    if selected_segments:
        filtered_data = seg[seg['segments'].isin(selected_segments)]

        fig = px.bar(
            filtered_data,
            x='segments',
            y='count',
            labels={'count':'عدد العملاء' ,'segments':'الفئة'},
            title='عدد العملاء في كل فئة',
            color_discrete_sequence=['#FF6000']
        ).update_layout(**common_layout)
        return fig
    return {}

@app.callback(
    Output('segment-table', 'data'),
    Input('segment-dropdown', 'value')
)

def update_segment_table(selected_segments):
    if selected_segments:
        selected_data = customer_purchase[customer_purchase['segments'].isin(selected_segments)][['رقم العميل', 'عدد الزيارات', 'معدل الشراء']]
        unique_data = selected_data.drop_duplicates(subset=['رقم العميل'])
        sorted_data = unique_data.sort_values(by=['عدد الزيارات','معدل الشراء'], ascending=[False,False])

        return sorted_data.head(10).to_dict('records')
    return []


@app.callback(
    Output('comp-plot', 'figure'),
    Input('comp-dropdown', 'value')
)



def update_comp_plot(selected_comp):

    if selected_comp:
        filtered_data = dep[dep['Department'].isin(selected_comp)]
        
        fig = px.bar(
            filtered_data,
            x='reason',  
            y='count',
            labels={'count':'عدد العملاء' ,'reason':'الأسباب'},
            title='اسباب شكاوي العملاء',
            color_discrete_sequence=['#FF6000']
        ).update_layout(**common_layout)
        
        return fig
    return {}



    
    
    
    
    
    
    
    
@app.callback(
    [Output('cat-plot1', 'figure'),Output('cat-plot2', 'figure'),Output('cat-plot3', 'figure'),Output('cat-plot4', 'figure')],
    Input('category-dropdown', 'value')
)



def update_cat_plot(selected_cat):
    if selected_cat:
        
        other_counts = merged_other.groupby(['segments', 'القسم السلعي']).size().reset_index(name='count')
        loyal_counts = merged_loyal.groupby(['segments', 'القسم السلعي']).size().reset_index(name='count')
        
        
        
        filtered_data = loyal_counts[loyal_counts['القسم السلعي'].isin(selected_cat)]
        filtered_data2 = other_counts[other_counts['القسم السلعي'].isin(selected_cat)]
        filtered_data3 = sales[sales['القسم السلعي'].isin(selected_cat)]
        filtered_data4 = category_merge[category_merge['القسم السلعي'].isin(selected_cat)]

        figure1 = px.bar(
            filtered_data,
            y='count', x='segments',
            labels={'count':'عدد العملاء' ,'segments':'الفئة'},color='القسم السلعي',
            color_discrete_sequence=custom_color_palette,
            title='المنتجات الأكثر مبيعًا لفئة المخلصين (Loyal)').update_layout(common_layout
        )
            
        figure2 = px.bar(
            filtered_data2,
            y='count', x='segments',labels={'count':'عدد العملاء' ,'segments':'الفئة'},color='القسم السلعي',
            color_discrete_sequence=custom_color_palette
            ,title='المنتجات الأكثر مبيعًا للفئات الآخرى').update_layout(**common_layout
        )
        
        figure3 = px.line(
            filtered_data3,
            x='الشهر ', y='المشتريات',color='القسم السلعي',title='نسبة المبيعات للاقسام السلعية لكل شهر',
            color_discrete_sequence=custom_color_palette).update_layout(**common_layout)
        
        
        
        figure4 = px.bar(
            filtered_data4,
            x='القسم السلعي',
            y=['عدد المنتجات', 'قيمة المشتريات'],
            barmode='group',
            labels={'value': 'قيمة المشتريات'},
            title='مقارنة بين عدد المنتجات وقيمتها حسب القسم السلعي ',
            color_discrete_sequence=custom_color_palette
        ).update_layout(common_layout
        )
        
        
        
        
        
        return figure1, figure2, figure3, figure4
    return {}, {}, {}, {}

if __name__ == '__main__':
    app.run_server(debug=True,port=8805)