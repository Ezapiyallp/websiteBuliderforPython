from PyQt5.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem ,QComboBox, QCheckBox


from mainWindow import Ui_MainWindow




class clsmainWindow(QMainWindow):
    def __init__(self):
        super(clsmainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn1.clicked.connect(self.btn1Click)
        self.ui.btn2.clicked.connect(self.btn2Click)


        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.verticalHeader().setVisible(0)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Coloum Name','Datatype','Control Type','Hide in UI'])
        self.ui.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.btnInsert.clicked.connect(self.btnInsertClick)
        self.ui.btnUpdate.clicked.connect(self.btnUpdateClick)
        self.ui.BtnDelete.clicked.connect(self.BtnDeleteClick)
        self.ui.btnLoadRecordInUI.clicked.connect(self.btnLoadRecordInUIClick)
        self.ui.btnLoadRecordInBootrapTable.clicked.connect(self.btnLoadRecordInBootrapTableClick)


    def btnInsertClick(self):
        JQCode=""
        dataToSend_midLine=""
        rw = self.ui.tableWidget.rowCount()
        for i in range(rw):

            try:
                col = self.ui.tableWidget.item(i, 0).text()
                controlType = self.ui.tableWidget.cellWidget(i, 2)
                if controlType.currentText() == "Text":
                    dataToSend_midLine += f"{col}: $('#txt{col}').val(),\n"
                if controlType.currentText() == "Select":
                    dataToSend_midLine +=  f"{col}: $('#sel{col}').val(),\n"
            except:
                pass

        dataToSend="const dataToSend = {\n"+dataToSend_midLine +" \n};"

        finalString=dataToSend+""" 
        tempid = $('#txtid').val()
        if (tempid === "") 
        {
            $.ajax({
            url: 'http://127.0.0.1:8000/api/save_in_"""+self.ui.txttableName.text() +"""', // API endpoint\n
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(dataToSend),
            headers: {
                'X-CSRFToken': '{{ csrf_token }}' // If CSRF is enabled in Django\n
            },
            success: function (response) {
                if (response.status === 'success') {
         
                } else {
           
                }
            },
            error: function (xhr) {   
            }
        });
    }
    else
    {
        $.ajax({
            url: 'http://127.0.0.1:8000/api/update_in_"""+self.ui.txttableName.text() +"""', // API endpoint\n
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(dataToSend),
            headers: {
                'X-CSRFToken': '{{ csrf_token }}' // If CSRF is enabled in Django\n
            },
            success: function (response) {
                if (response.status === 'success') {
         
                } else {
           
                }
            },
            error: function (xhr) {   
            }
        });
    }
      """
        self.ui.txtAJAXPost.setPlainText(finalString)
        APIVeriableList=""

        rw = self.ui.tableWidget.rowCount()
        for i in range(rw):
            try:
                col = self.ui.tableWidget.item(i, 0).text()
                APIVeriableList+=f"{col} = data.get('{col}', None)\n"
            except:
                pass
        tempInsert=""
        for i in range(rw):
            try:
                if i< rw-1:
                    col = self.ui.tableWidget.item(i, 0).text()
                    tempInsert+=f"'\"+{col}+\"',"
                else:
                    col = self.ui.tableWidget.item(i, 0).text()
                    tempInsert += f"'\"+{col}+\"'"
            except:
                pass


        APIInsertStatment = "insert into " + self.ui.txttableName.text() + " values("+tempInsert+")"

        APIString="""@csrf_exempt
@require_POST
def save_in_""" + self.ui.txttableName.text() + """(request):
    try:
        data = json.loads(request.body)\n
        """ + APIVeriableList + """
        \n\t\tdb = sqlite3.connect('db.sqlite3')
        cursor = db.cursor() \n cursor.execute(\"
        """ + APIInsertStatment + """ \")
        \n\t\tdb.commit()
        response_data = {'status': 'success', 'message': 'Record Save in Database'}
        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
"""


        tempUpdate = ""
        for i in range(rw):
            try:
                if i < rw - 1:
                    col = self.ui.tableWidget.item(i, 0).text()
                    tempUpdate += f"{col}='\"+{col}+\"',"

                else:
                    col = self.ui.tableWidget.item(i, 0).text()
                    tempUpdate += f"{col}='\"+{col}+\"'"
            except:
                pass

        APIUpdateStatment = f"update  " + self.ui.txttableName.text() + " set "+tempUpdate+" where id=+str(id)"

        APIUpdateString = """@csrf_exempt
        @require_POST
        def update_in_""" + self.ui.txttableName.text() + """(request):
            try:
                data = json.loads(request.body)\n
                """ + APIVeriableList + """
                \n\t\tdb = sqlite3.connect('db.sqlite3')
                cursor = db.cursor() \n cursor.execute(\"
                """ + APIUpdateStatment + """ \")
                \n\t\tdb.commit()
                response_data = {'status': 'success', 'message': 'Record Save in Database'}
                return JsonResponse(response_data)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        """


        self.ui.txtpythonAPI.setPlainText(APIString+"\\n"+APIUpdateString)
    

    def btnUpdateClick(self):
        pass
    def BtnDeleteClick(self):
        JQDelete="""
        function funDelete(myId) {
            $('#txtid').val(myId);
            const dataToSend = {
                id: $('#txtid').val(),
            };
            $.ajax({
                url: 'http://127.0.0.1:8000/api/delete_in_"""+self.ui.txttableName.text() +"""', // API endpoint

                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}' // If CSRF is enabled in Django

                },
                success: function (response) {
                   
                },
                error: function (xhr) {
                }
            });
        }
"""
        self.ui.txtAJAXPost.setPlainText(JQDelete)
        APIUpdate="""
@csrf_exempt
@require_POST
def delete_in_"""+ self.ui.txttableName.text()+"""(request):
    try:
        data = json.loads(request.body)

        id = data.get('id', None)
       
        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor() 
        sql=f"delete from  """+ self.ui.txttableName.text()+"""  where id="+str(id)
        cursor.execute(sql)
        
        db.commit()
        response_data = {'status': 'success', 'message': 'Record Save in Database'}
        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        """
        self.ui.txtpythonAPI.setPlainText(APIUpdate)
    def btnLoadRecordInUIClick(self):

        # $('#txtid').val(response[0].id);


        tempUI = ""

        rw = self.ui.tableWidget.rowCount()
        for i in range(rw):
            try:
                col = self.ui.tableWidget.item(i, 0).text()
                tempUI+=f"$('#txt{col}').val(response[0].{col});\n"

            except:
                pass
        loadString="""
function funEdit(myId) {
            $('#txtid').val(myId);
            const dataToSend = {
                id: $('#txtid').val(),
            };
            $.ajax({
                url: 'http://127.0.0.1:8000/api/getSingle_Record_from_"""+ self.ui.txttableName.text() +"""', // API endpoint

                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}' // If CSRF is enabled in Django

                },
                success: function (response) {
                    // alert(response[0].rollno);
                    """+tempUI+"""
                },
                error: function (xhr) {
                }
            });
        }
        """
        self.ui.txtAJAXPost.setPlainText(loadString)
        loadAPI="""
@csrf_exempt
@require_POST
def getSingle_Record_from_"""+ self.ui.txttableName.text() +"""(request):
    try:
        data = json.loads(request.body)
        id = data.get('id', None)

        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM """+ self.ui.txttableName.text() +""" where id="+str(id))  # Replace with your table name
        columns = [col[0] for col in cursor.description]  # Extract column names
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert rows to dictionaries
        return JsonResponse(data, safe=False)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)       
        """
        self.ui.txtpythonAPI.setPlainText(loadAPI)
    def btnLoadRecordInBootrapTableClick(self):
        UiCode = ""
        tableCol=""
        rw = self.ui.tableWidget.rowCount()
        for i in range(rw):

            try:
                col = self.ui.tableWidget.item(i, 0).text()
                tableCol+=f"""
                    <th data-field='{col}' data-sortable='true'>
            <span class='text-success'>
              {col}
            </span>
          </th>
                """
            except:
                pass
        tableCol += f"""
                            <th data-field='actions' data-sortable='true'>
                    <span class='text-success'>
                      Action
                    </span>
                  </th>
                        """

        UiCode=f"""
         <div class='container text-light'>
    <table id='myTable' class='table-striped table-dark border-success' data-search='true' data-flat='true'
      data-show-header='true' data-pagination='true' data-page-list='[5, 10, 25, 50, 100, ALL]' data-page-size='10'>
      <thead>
        <tr>
              {tableCol}        
       </tr>
      </thead>
    </table>
  </div>
         """
        self.ui.txtUICode.setPlainText(UiCode)
        pythonAPICode=""" 
        @csrf_exempt
def getAll_Record_from_"""+self.ui.txttableName.text()+"""(request):
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM """+self.ui.txttableName.text() +""" ")  # Replace with your table name
    columns = [col[0] for col in cursor.description]  # Extract column names
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert rows to dictionaries
    
    for player in data:
        player_id = player["id"]
        player["actions"] = f'''
        <button class='btn btn-primary btn-sm edit-btn' data-id='{player_id}' onclick='funEdit({player_id})'>Edit</button>
        <button class='btn btn-danger btn-sm delete-btn' data-id='{player_id}' onclick='funDelete({player_id})'>Delete</button>
        '''
    return JsonResponse(data, safe=False)
        
        """
        self.ui.txtpythonAPI.setPlainText(pythonAPICode)
        JQCode=""" 
        $.ajax({
      cache: false,
      async: false,
      type: "POST",
      url: 'http://127.0.0.1:8000/api/getAll_Record_from_"""+self.ui.txttableName.text()+"""',
      data: {

      },
      dataType: "json",
      success: function (result) {
        $('#myTable').bootstrapTable({
          data: result
        });

      },
    });
        """
        self.ui.txtAJAXPost.setPlainText(JQCode)
    def btn1Click(self):
        self.ui.tableWidget.setRowCount(0)
        tableData= self.ui.txtTableStruture.toPlainText()
        tableData= tableData.split('\n')
        print(tableData[0])
        tablename = str(tableData[0]).split("\"")
        self.ui.txttableName.setText(tablename[1])

        if tableData[-2] != 'PRIMARY KEY("id" AUTOINCREMENT)':
            for i in range(1, len(tableData)-2):
                self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount() + 1)
                rw = self.ui.tableWidget.rowCount()
                # print(tableData[i])
                try:

                    colData=str(tableData[i]).split('\t')
                    colData[1]=str(colData[1]).replace("\"","")
                    colData[2] = str(colData[2]).replace(",", "")
                    combo_box = QComboBox()
                    combo_box.addItems(["Text", "Select"])
                    chk = QCheckBox()
                    self.ui.tableWidget.setItem(rw - 1, 0, QTableWidgetItem(colData[1]))
                    self.ui.tableWidget.setItem(rw - 1, 1, QTableWidgetItem(colData[2]))

                    self.ui.tableWidget.setCellWidget(rw -1 , 2, combo_box)
                    self.ui.tableWidget.setCellWidget(rw - 1, 3, chk)

                except Exception as e:
                    print(e)
        else:
            for i in range(1, len(tableData) - 1):
                self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount() + 1)
                rw = self.ui.tableWidget.rowCount()
                # print(tableData[i])
                try:

                    colData = str(tableData[i]).split('\t')
                    colData[1] = str(colData[1]).replace("\"", "")
                    colData[2] = str(colData[2]).replace(",", "")
                    combo_box = QComboBox()
                    combo_box.addItems(["Text", "Select"])
                    chk = QCheckBox()
                    self.ui.tableWidget.setItem(rw - 1, 0, QTableWidgetItem(colData[1]))
                    self.ui.tableWidget.setItem(rw - 1, 1, QTableWidgetItem(colData[2]))

                    self.ui.tableWidget.setCellWidget(rw - 1, 2, combo_box)
                    self.ui.tableWidget.setCellWidget(rw - 1, 3, chk)

                except Exception as e:
                    print(e)



    def btn2Click(self):

        if self.ui.chkSideBySide.isChecked():
            UIData=""
            rw = self.ui.tableWidget.rowCount()
            for i in range(rw):
                try:
                    controlData=""
                    col = self.ui.tableWidget.item(i, 0).text()
                    dataType = self.ui.tableWidget.item(i, 1).text()
                    controlType = self.ui.tableWidget.cellWidget(i, 2)
                    if controlType.currentText()=="Text":
                        controlData = f"<input type='text' class='form-control' id='txt{col}'>"
                    if controlType.currentText() == "Select":
                        controlData = f"""<select id='sel{col}' class='form-select' aria-label='Default select example'>
                          <option selected>Open this select menu</option>
                          <option value='1'>One</option>
                          <option value='2'>Two</option>
                          <option value='3'>Three</option>
                        </select>"""
                    hideStatus = self.ui.tableWidget.cellWidget(i, 3)
                    if hideStatus and isinstance(hideStatus, QCheckBox):
                        is_checked = hideStatus.isChecked()  # True or False
                    else:
                        is_checked = False
                    rowData = f"""<div class='row m-2 p-2'>
                        <div class='col-sm'><label>Enter Value of {col}  </label> </div>
                        <div class='col-sm'>{controlData}</div>
                    </div>"""
                    UIData+=rowData

                except:
                    pass

            self.ui.txtUICode.setPlainText(UIData)


        else:
            UIData = ""
            rw = self.ui.tableWidget.rowCount()
            for i in range(rw):
                try:
                    controlData = ""
                    col = self.ui.tableWidget.item(i, 0).text()
                    dataType = self.ui.tableWidget.item(i, 1).text()
                    controlType = self.ui.tableWidget.cellWidget(i, 2)
                    hideStatus = self.ui.tableWidget.cellWidget(i, 3)
                    if hideStatus and isinstance(hideStatus, QCheckBox):
                        is_checked = hideStatus.isChecked()  # True or False
                    else:
                        is_checked = False
                    if controlType.currentText() == "Text":
                        controlData = f" <input type='text' class='form-control col-sm-6' id='txt{col}' />"
                    if controlType.currentText() == "Select":
                        controlData = f"""<select id='sel{col}' class='form-select col-sm-6' aria-label='Default select example'>
                                     <option selected>Open this select menu</option>
                                     <option value='1'>One</option>
                                     <option value='2'>Two</option>
                                     <option value='3'>Three</option>
                                   </select>"""
                    rowData = f"""<div class='m-3'>
                            <label class='form-label'>Enter Value of {col}</label>
                            {controlData}
                            </div>"""
                    UIData += rowData
                except:
                    pass

            self.ui.txtUICode.setPlainText(UIData)




    def btn3Click(self):
        pass