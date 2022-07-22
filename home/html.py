html_home = ("""
    <style>
        h1,h2,h3,h4,h5,h6 {
        color: #006699;
        }

        p {
        line-height: 1.5;
        }

        .main {
        font-size: 15px;
        padding: 10px;
        }

        .dropdown {
        list-style-type: none;
        }
    </style>
    <h1>Welcome to NWB Scheduler</h1>
    <div class="main">
    <p>This is a scheduler application to assist responsible brothers 
    in the congregation to create and manage <strong>our christian and life ministry meeting.</strong>
    This Software is in <strong>No way related or backed by the
    Watchtower Bible And Track Society</strong>. Rather it's a tool to make life easier for brothers in charge
    of designing the Meeting WorkBook program for their respective congregations. Read More about this in the <strong>Terms and Conditions</strong>.
    Now Read the Usage Guide below to get started</p>

    <h2>NWB Scheduler - Usage</h2>
    <ol>
        <li><b>Home</b>
            <ul class="dropdown">
                <li>You are on the home page currently! Brief details about the software</li>
            </ul>
        </li>
        <li><b>Congregation</b>
            <ul class="dropdown">
                <li>Create a congregation Database so you can easily make NWB meetings programs.
                Add, remove and modify members of the congregation</li>
                </li>
            </ul>
        </li>
        <li><b>Scheduler</b>
            <ul class="dropdown">
                <li>With a click of a button, you can get a generated program and see it's preview.
                select the program format and generate a program or simply use the auto generate and save the program
                as a pdf file on your computer</li>
            </ul>
        </li>
        <li><b>Reports</b>
            <ul class="dropdown">
                <li>View Previous created meeting programs and make modifications on the fly. If 
                you made an error, adjusting it is a piece of cake.</li>
            </ul>
        </li>
    </ol>

    <h2 style="text-align: left;">NWB Scheduler - Features</h2>
    <ol>
        <li>Create a Congregation Database</li>
        <li>Assign Congregation Roles
        <ul>
            <li>Elder</li>
            <li>Ministerial Servant</li>
        </ul>
        </li>
        <li>Auto Assign Meeting Parts And Student Parts</li>
        <li>Download as a PDF</li>
        <li>Backup Settings and Congregation Data</li>
    </ol>

    </div>
    
    """)


default_program_html = '''
<html>
<head>
    <title>S-140-PGW</title>
    <style>
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
    </style>
</head>

<body>
    <div class="header">
        <div class="titles">
            <h4>BONENDALE PIDGIN</h4>
            <h2>OUR CHRISTIAN LIFE AND PREACHING MEETING</h2>
        </div>
        <div class="line1"></div>
    </div>
    {% for d, program in zip(data.values(), programs.values()) %}
    <table class="table" style="table-layout: fixed; page-break-after: always">
        <tr>
            <td class="tdfix"><strong class="date">{{ d.month }}</strong> | <strong
                    class="emph">{{ d['reading'] }}</strong></td>
            <td class="tdfix2"><a class="right nwb-roles">Chairman:</a></td>
            <td style="width: 250px;"><strong>{{ program["chairman"].split(" ")[0].upper() }}
                    {{ program["chairman"].split(" ")[1].capitalize() }}</strong></td>
        </tr>
        <tr>
            <td>6:30<i>&#9679;</i><strong class="emph">{{ d['opening_song'] }}</strong></td>
            <td><a class="right nwb-roles">Prayer:</a></td>
            <td><a>{{ program["opening_prayer"].split(" ")[0].upper() }} {{ program["opening_prayer"].split(" ")[1].capitalize() }}
                    {% if program["opening_prayer"].split(" ")[2] %}{{ program["opening_prayer"].split(" ")[2].capitalize() }}{% endif %}</a>
            </td>
        </tr>
        <tr>
            <td>6:36<i>&#9679;</i><strong> Wetin We Go Learn? (1 min.)</strong></td>
            <td></td>
            <td><strong>{{ program["chairman"].split(" ")[0].upper() }}
                    {{ program["chairman"].split(" ")[1].capitalize() }}</strong></td>
        </tr>
        <tr>
            <td colspan="1" style="background-color: rgb(87,90,93); height: 30px; break-inside: avoid;"><a
                    class="nwb-title heading">FINE-FINE LESSON FROM BIBLE</a></td>
            <td class="nwb-roles">{{ program["group"].split(" ")[0].upper() }}{% if program["group"].split(" ")[1] %}
                {{ program["group"].split(" ")[1].upper() }}{% endif %} Group</td>
            <td><a class="nwb-roles">Main Hall</a></td>
        </tr>
        <tr>
            <td>6:39<i style="color: rgb(87,90,93);">&#9679;</i><strong
                    class="emph">{{ d['fine_fine_lesson'] }}</strong>(10 min.)</td>
            <td></td>
            <td>{{ program["fine_fine_lesson"].split(" ")[0].upper() }} {{ program["fine_fine_lesson"].split(" ")[1].capitalize() }}</td>
        </tr>
        <tr>
            <td>6:49<i style="color: rgb(87,90,93);">&#9679;</i><strong>Fine-Fine Things Wey You See for
                    Bible:</strong>(10 min.)</td>
            <td></td>
            <td>{{ program["fine_fine_things_weh_you_see"].split(" ")[0].upper() }} {{ program["fine_fine_things_weh_you_see"].split(" ")[1].capitalize() }}</td>
        </tr>
        <tr>
            <td>6:57<i style="color: rgb(87,90,93);">&#9679;</i><strong>Bible Reading (<a
                        class="emph">{{ d['bible_reading_point'].strip("th study") }}</a>): (4 min.)</strong>
                <a class="right nwb-roles">Student:</a></td>
            <td>{% if program["bible_reading_s"] %}
                {{ program["bible_reading_s"].split(" ")[0].upper() }}
                {{ program["bible_reading_s"].split(" ")[1].capitalize() }}</td>
            {% endif %}
            <td>{{ program["bible_reading"].split(" ")[0].upper() }} {{ program["bible_reading"].split(" ")[1].capitalize() }}</td>
        </tr>
        <tr>
            <td colspan="1" class="tdfix" style="background-color: rgb(190,137,0); height: 30px;"><a
                    class="nwb-title heading">DE USE ALL YOUR HEART PREACH</a></td>
            <td class="nwb-roles"></td>
            <td class="nwb-roles">Main Hall</td>
        </tr>
        {% for step, parts in zip2(d['preaching']) %}
        <tr>
            <td>7:{% if step == 0 %}
                02
                {% elif preachingt[step-1] >= 10 %}
                {{ preachingt[step-1] }}
                {% else %}
                0{{ preachingt[step-1] }}
                {% endif %}<i style="color: rgb(190,137,0);">&#9679;</i>
                <strong>{{ parts.strip(":") }}
                    {% if d['preaching_points'][step] == "" %}
                    {% else %}
                    (<a class="emph">{{ d['preaching_points'][step] }}</a>)
                    {% endif %}
                    : ({{ d['preaching_time'][step] }} min.)</strong>
                {% if parts.strip(":").endswith("Video") %}

                {% elif length(vid) > 23 %}

                {% elif parts.strip(":") == "Talk" %}

                {% else %}
                <a class="right nwb-roles">Student:<br>Assistant:</a>
                {% endif %}
            </td>
            <td>{% if program["preaching_s"] %}
                {{ program["preaching_s"][step].split("/")[0].split(" ")[0].upper() }}
                {{ program["preaching_s"][step].split("/")[0].split(" ")[1].capitalize() }}
                {% if program["preaching"][step].split("/")[0].split(" ")[2] %}
                {{ program["preaching"][step].split("/")[0].split(" ")[2].capitalize() }}{% endif %}<br>
                {{ program["preaching_s"][step].split("/")[1].split(" ")[0].upper() }}
                {{ program["preaching_s"][step].split("/")[1].split(" ")[1].capitalize() }}
                {% if program["preaching"][step].split("/")[1].split(" ")[2] %}
                {{ program["preaching"][step].split("/")[1].split(" ")[2].capitalize() }}{% endif %}
                {% else %}
                Hello<br>
                World
                {% endif %}
            </td>
            <td> {% if program["preaching"][step].split("/")[1] %}
                <a>{{ program["preaching"][step].split("/")[0].split(" ")[0].upper() }}
                    {{ program["preaching"][step].split("/")[0].split(" ")[1].capitalize() }}
                    {% if program["preaching"][step].split("/")[0].split(" ")[2] %}
                    {{ program["preaching"][step].split("/")[0].split(" ")[2].capitalize() }}{% endif %}</a><br>
                <a>{{ program["preaching"][step].split("/")[1].split(" ")[0].upper() }}
                    {{ program["preaching"][step].split("/")[1].split(" ")[1].capitalize() }}
                    {% if program["preaching"][step].split("/")[1].split(" ")[2] %}
                    {{ program["preaching"][step].split("/")[1].split(" ")[2].capitalize() }}{% endif %}</a>
                {% else %}
                <a>{{ program["preaching"][step].split("/")[0].split(" ")[0].upper() }}
                    {{ program["preaching"][step].split("/")[0].split(" ")[1].capitalize() }}
                    {% if program["preaching"][step].split("/")[0].split(" ")[2] %}
                    {{ program["preaching"][step].split("/")[0].split(" ")[2].capitalize() }}{% endif %}</a><br>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
        <tr>
            <td colspan="1" class="tdfix" style="background-color: rgb(126,0,36); height: 30px;"><a
                    class="nwb-title heading">DE LIVE CHRISTIAN LIFE</a>
            </td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>7:17<i style="color: rgb(126,0,36);">&#9679;</i><strong
                    class="emph">{{ d['middle_song'] }}</strong></td>
            <td></td>
            <td></td>
        </tr>
        {% for step, lac in zip2(d['middle_parts']) %}
        <tr>
            <td>7:{% if step == 0 %}
                21
                {% else %}
                {{ middlepartst[step-1] }}
                {% endif %}<i style="color: rgb(126,0,36);">&#9679;</i><strong>{{ lac.strip(":") }}:
                    ({{ d['middle_parts_time'][step] }} min.)</strong></td>
            <td></td>
            <td><strong>{% if program["middle_parts"][step] %}{{ program["middle_parts"][step].split(" ")[0].upper() }}
                    {{ program["middle_parts"][step].split(" ")[1].capitalize() }}{% endif %}</strong></td>
        </tr>
        {% endfor %}
        <tr>
            <td>7:36<i style="color: rgb(126,0,36);">&#9679;</i><strong>Congregation Bible Study <a
                        class="emph">({{ d['book_study'] }}):</a> (30 min.)</strong></td>
            <td><a class="right nwb-roles">Conductor/Reader:</a></td>
            <td><a>{{ program["cong_bible_study"].split("/")[0].split(" ")[0].upper() }}
                    {{ program["cong_bible_study"].split("/")[0].split(" ")[1].capitalize() }}/
                    {% if program["cong_bible_study"].split("/")[1] %}
                    {{ program["cong_bible_study"].split("/")[1].split(" ")[0].upper()  }}
                    {{ program["cong_bible_study"].split("/")[1].split(" ")[1].capitalize() }}
                    {% endif %}
                </a></td>
        </tr>
        <tr>
            <td>8:06<i style="color: rgb(126,0,36);">&#9679;</i><strong>Wetin We Don Learn (3 min.)</strong></td>
            <td></td>
            <td><strong>{{ program["chairman"].split(" ")[0].upper() }}
                    {{ program["chairman"].split(" ")[1].capitalize() }}</strong></td>
        </tr>
        <tr>
            <td>8:09<i style="color: rgb(126,0,36);">&#9679;</i><strong class="emph">Song 113</strong></td>
            <td><a class="right nwb-roles">Prayer:</a></td>
            <td><a>{{ program["closing_prayer"].split(" ")[0].upper() }} {{ program["closing_prayer"].split(" ")[1].capitalize() }}</a></td>
        </tr>
    </table><br>
    {% endfor %}
    <!--<h3>NB: All publishers wey e get assignment go attend meeting for <b>kingdom hall for that very week</b> for present
        thier assignment, and make them always check the attached program.</h3> -->
</body>

</html>
'''