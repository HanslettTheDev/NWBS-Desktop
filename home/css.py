congregation_view_css = ('''
#cong_button_1, #cong_button_2 {
    background-color: white;
    font-size: 15px;
}
''')

button_frame = ('''
QPushButton {
    font-size: 15px;
}
''')

pdf_css = '''
    @font-face {
        font-family: 'Gaduji';
        src: url("fonts/Gadugi/gadugi-normal.ttf");
    }

    @font-face {
        font-family: 'Gaduji-bold';
        src: url("fonts/Gadugi/gadugi-bold.ttf");
    }

    body {
        font-family: 'Gaduji', sans-serif;
        font-style: normal;
        box-sizing: border-box;
    }

    tr,
    td,
    table {
        border: 1px solid white;
    }

    .header {
        width: 1000px;
        height: 80px;
        overflow: hidden;
        /* margin-left: auto;
margin-right: auto; */
    }

    .header h4,
    .date {
        font-family: 'Gaduji-bold';
        font-weight: bolder;
    }

    .header h2 {
        font-family: 'Gaduji-bold';
        color: #0078d7;
    }

    .titles {
        max-width: inherit;
        height: 55px;
        display: flex;
        justify-content: space-around;
    }

    .titles h4 {
        margin-right: 120px;
        font-size: 18px;
    }

    .titles h2 {
        margin-bottom: 5%;
    }


    .line1 {
        width: 1000px;
        height: 2px;
        border-top: 2px solid black;
        border-bottom: 2px solid black;
    }

    .table {
        width: 900px;
        /* margin-left: auto;
margin-right: auto; */
        font: 12px;
    }

    .tdfix {
        width: 550px;
        overflow: auto;
        white-space: nowrap;
    }

    .tdfix2 {
        width: 200px;
        overflow: auto;
        white-space: pre-line;
    }

    i {
        font-size: 15px;
        padding: 1%;
    }

    .heading {
        margin-left: 5px;
    }

    .control>td {
        width: 100px;
    }

    .img {
        height: 80px;
    }

    .nwb-roles {
        color: rgb(87, 90, 93);
        font-weight: bold;
    }

    .nwb-title {
        font-family: 'Gaduji-bold';
        font-size: 18px;
        font-weight: 700;
        color: white;
    }

    .left {
        float: left;
    }

    .right {
        float: right;
    }

    .emph {
        color: #0078d7;
        font-weight: bold;
    }

    .color-scheme1 i {}

    .color-scheme2 i {
        color: rgb(190, 137, 0);
    }

    .color-scheme3 i {
        color: rgb(126, 0, 36);
    }
'''