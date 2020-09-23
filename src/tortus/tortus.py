import pandas as pd
from datetime import datetime
import sysconfig
from ipywidgets import Image, HTML, Button, IntProgress, \
    Box, HBox, VBox, GridBox, Layout, ButtonStyle, Output
from IPython.display import SVG, HTML, display, clear_output


package_dir = sysconfig.get_paths()['purelib']
logo_path = package_dir + '/tortus/tortus_logo.png'

with open(logo_path, 'rb') as image_file:
    image = image_file.read()

logo = Image(value=image, format='png', width='100%')

welcome = HTML("<h2 style='text-align:center'>easy text annotation in a Jupyter Notebook</h2>")
display(logo, welcome)

class Tortus:
    '''Text annotation within a Jupyter Notebook
    
    :attr annotation_index: A counter for the annotations in progress

    :param df: A dataframe with texts that need to be annotated
    :type df: pandas.core.frame.DataFrame

    :param text: The name of the column containing the text to be annotated
    :type text: str

    :param num_records: Number of records to annotate, defaults to 10
    :type num_records: int, optional
    
    :param id_column: The name of the column containing ID of the text - if None, ``id_column`` 
        is the index of ``df``, default is None
    :type id_column: str, optional

    :param annotations: The dataframe with annotations previously created in this tool.
        If None, ``annotations`` is created with columns ``id_column``, ``text``, ``label``, 
        ``annotated_at``, default is None
    :type annotation_df: pandas.core.frame.DataFrame, optional

    :param random: Determines if records are loaded randomly or sequentially, default is True
    :type random: bool, optional

    :param labels: Annotation labels, default is ['Positive', 'Negative', 'Neutral']
    :type labels: list, optional
    '''
    annotation_index = 0


    def __init__(self, df, text, num_records=10, id_column=None, annotations=None, random=True,
                labels=['Positve', 'Negative', 'Neutral']):
        '''Initializes the Tortus class.'''
        self.df = df
        self.text = text
        self.num_records = num_records
        self.id_column = id_column
        if annotations is None:
            if id_column is None:
                self.annotations = pd.DataFrame(columns=['id_column', text, 'label', 'annotated_at'])
            else:
                self.annotations = pd.DataFrame(columns=[id_column, text,'label','annotated_at'])
        else:
            self.annotations = annotations.copy()
        self.random = random
        self.labels = labels
        self.subset_df = self.create_subset_df()


    def create_subset_df(self):
        '''
        Subsets ``df`` to include only records cued for annotation.

        If ``annotations`` already exists, those records will excuded from the annotation tool.

        :returns: A dataframe that will be used in the annotation tool.
        :rtype: pandas.core.frame.DataFrame
        '''
        if self.annotations.empty:
            subset_df = self.df.copy()

        else:
            leave_out = self.annotations[self.text].to_list()
            subset_df = self.df[~self.df[self.text].isin(leave_out)]

        if self.random:
            try:
                subset_df = subset_df.sample(n=self.num_records)[[self.id_column, self.text]]
            except:
                subset_df = subset_df.sample(n=self.num_records)[[self.text]]
        else:
            try:
                subset_df = subset_df[[self.id_column, self.text]][:self.num_records]
            except:
                subset_df = subset_df[[self.text]][:self.num_records]

        return subset_df


    def create_record_id(self):
        '''Provides a record id for ``annotations``.

        :returns: A list of record ids that refer to each text in subset df created by 
            :meth:`create_subset_df` method.
        :rtype: list
        '''
        if self.id_column is None:
            record_id = self.subset_df.index.to_list()
        else:
            record_id = self.subset_df[self.id_column].to_list()
        return record_id

    def make_html(self, text):
        '''Changes text to html for annotation widget user interface.

        :param text: Text for conversion to html.
        :type text: str

        :returns: HTML snippet
        :rtype: str
        '''
        html = '<h4>' + text + '</h4>'
        return html

    def annotate(self):
        '''Displays texts to be annotated in a UI. Loads user inputted labels and timestamps into
            ``annotations`` dataframe.
        '''
        with open(logo_path, 'rb') as image_file:
            image = image_file.read()
            logo = Image(value=image, format='png', width='40%')

        rules = HTML(
            'Click on the label corresponding with the text below. Each selection requires \
                confirmation before proceeding to the next item.')
        annotation_text = self.subset_df.iloc[self.annotation_index, -1]
        html = self.make_html(annotation_text)
        text = HTML(html)
        
        labels = []
        for label in self.labels:
            label_button = Button(
                description=label,
                layout=Layout(border='solid', flex='1 1 auto', width='auto'),
                style=ButtonStyle(button_color='#eeeeee', font_weight='bold'))
            labels.append(label_button)

        label_buttons = HBox(labels)
        
        skip_button = Button(
            description='Skip',
            layout=Layout(border='solid', flex='1 1 auto', width='auto'),
            style=ButtonStyle(button_color='#eeeeee', font_weight='bold'))
       
        confirm_button = Button(
            description='Confirm selection',
            layout=Layout(border='solid', flex='1 1 auto', width='auto', grid_area='confirm'),
            style=ButtonStyle(button_color='#eeeeee', font_weight='bold'))
        
        redo_button = Button(
            description='Try again',
            layout=Layout(border='solid', flex='1 1 auto', width='auto', grid_area='redo'),
            style=ButtonStyle(button_color='#eeeeee', font_weight='bold'))
        
        progress_bar = IntProgress(
                value=self.annotation_index,
                min=0,
                max=self.num_records,
                step=1,
                description=f'{self.annotation_index + 1}/{self.num_records}',
                bar_style='',
                orientation='horizontal',
                layout=Layout(width='50%', align_self='flex-end'))
        progress_bar.style.bar_color = '#36a849'
    
        header = HBox([logo, progress_bar])
        sentiment_buttons = HBox([label_buttons, skip_button])
        confirmation_buttons = HBox([confirm_button, redo_button])
        sentiment = labels + [skip_button]
        confirm = [confirm_button, redo_button]

        box_layout = Layout(
            display='flex',
            flex_flow='row',
            align_items='stretch',
            width='100%'
        )

        box_sentiment = Box(sentiment, layout=box_layout)
        box_confirm = Box(confirm, layout=box_layout)

        all_buttons = VBox(
            [box_sentiment, box_confirm],
            layout=Layout(width='auto', grid_area='all_buttons')
        )

        ui = GridBox(
            children=[all_buttons],
            layout=Layout(
                width='100%',
                grid_template_rows='auto auto',
                grid_template_columns='15% 70% 15%',
                grid_template_areas='''
                ". all_buttons ."
                ''')
        )
        
        output = Output()

        display(header, rules, text, ui, output)
        confirm_button.layout.visibility = 'hidden'
        redo_button.layout.visibility = 'hidden'    


        def label_buttons_clicked(button):
            '''Response to button click of any sentiment buttons.
            
            Appends ``annotations`` with label selection.
            :param button: Label buttons click. 
            '''
            button.style.button_color = '#36a849'
            record_id = self.create_record_id()
            self.annotations.loc[len(self.annotations)] = [
                record_id[self.annotation_index],
                self.subset_df[self.text].iloc[self.annotation_index],
                str(button.description).lower(),
                datetime.now().replace(microsecond=0)  
            ]
            
            for label in labels:
                label.disabled = True
                if button != label:
                    label.layout.border = 'None'

            skip_button.disabled = True
            skip_button.layout.border = 'None'
                
            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'visible'
                confirm_button.layout.visibility = 'visible'
                redo_button.layout.visibility = 'visible'

        for label in labels:
            label.on_click(label_buttons_clicked)
        

        def skip_button_clicked(button):
            '''Response to button click of the skip button.

            Appends ``annotations``. Label value is ``Null``.
            
            :param button: Skip button click.
            '''
            button.style.button_color = '#36a849'
            record_id = self.create_record_id()
            self.annotations.loc[len(self.annotations)] = [
                record_id[self.annotation_index],
                self.subset_df[self.text].iloc[self.annotation_index],
                None,
                datetime.now().replace(microsecond=0)  
            ]
            for label in labels:
                label.disabled = True
                label.layout.border = 'None'

            skip_button.disabled = True
                
            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'visible'
                confirm_button.layout.visibility = 'visible'
                redo_button.layout.visibility = 'visible'
            
        skip_button.on_click(skip_button_clicked)


        def confirm_button_clicked(button):
            '''Response to click of the confirm button.

            Advances the ``annotation_index`` to view the next item in the annotation tool.
                Indicates the tool is done if ``annotation_index`` does not advance further.
            
            :param button: Confirmation button click.
            '''
            if self.annotation_index < len(self.subset_df) - 1:
                self.annotation_index += 1
                clear_output(True)
                self.annotate()
            else:

                clear_output(True)
                progress_bar.value = self.num_records
                progress_bar.description = 'Complete'
                display(header, output)    

        confirm_button.on_click(confirm_button_clicked)


        def redo_button_clicked(button):
            '''Response to click of the redo button.

            Deletes the most recent input to ``annotations``.
            
            :param button: Redo button click.
            '''
            self.annotations.drop([self.annotation_index], inplace=True)
            for label in labels:
                label.style.button_color = '#eeeeee'
                label.disabled = False
                label.layout.border = 'solid'
                
            skip_button.style.button_color = '#eeeeee'
            skip_button.disabled = False
            skip_button.layout.border = 'solid'

            with output:
                clear_output(True)
                sentiment_buttons.layout.visibility = 'visible'
                confirm_button.layout.visibility = 'hidden'
                redo_button.layout.visibility = 'hidden'

        redo_button.on_click(redo_button_clicked)

