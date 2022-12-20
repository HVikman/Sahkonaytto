def wlansettings():
    html = f"""
        <!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="icon" href="data:," />
<style>
input[type="text"],
select {{
width: 100%;
padding: 12px 20px;
margin: 8px 0;
display: inline-block;
border: 1px solid #ccc;
border-radius: 4px;
box-sizing: border-box;
}}

button[type="submit"] {{
width: 100%;
background-color: #4caf50;
color: white;
padding: 14px 20px;
margin: 8px 0;
border: none;
border-radius: 4px;
cursor: pointer;
}}

button[type="submit"]:hover {{
background-color: #45a049;
}}

div {{
border-radius: 5px;
background-color: #f2f2f2;
padding: 20px;
}}
</style>
</head>
<body>
<center><h1>Wifi settings</h1></center>
<br /><br />
<form action="./" method="GET">
<center>
<div>
  <label for="ssid">SSID</label>
  <input type="text" name="ssid" id="ssid" value="" />
</div>
<div>
  <label for="to">Password</label>
  <input type="text" name="password" id="password" value="" />
</div>
<div>
  <button type="submit">Save and restart</button>
</div>
</center>
</form>
</body>
</html>

        """
    return str(html)
def settings(version):
    html = f"""
        <!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="icon" href="data:," />
    <style>
      body {{
        max-width: 500px;
        margin: auto;
      }}
      input[type="text"],
      select {{
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        display: inline-block;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
      }}

      button[type="submit"] {{
        width: 100%;
        background-color: #4caf50;
        color: white;
        padding: 14px 20px;
        margin: 8px 0;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }}

      button[type="submit"]:hover {{
        background-color: #45a049;
      }}

      div {{
        border-radius: 5px;
        background-color: #f2f2f2;
        padding: 20px;
      }}
      .accordion {{
        background-color: #4caf50;
        color: #444;
        cursor: pointer;
        padding: 18px;
        width: 100%;
        border: none;
        text-align: center;
        outline: none;
        font-size: 15px;
        transition: 0.4s;
        border: 1px solid #ccc;
        border-radius: 4px;
      }}

      .active,
      .accordion:hover {{
        background-color: #45a049;
      }}

      .panel {{
        padding: 0 18px;
        border-radius: 5px;
        background-color: #f2f2f2;
        max-height: 0;
        overflow: hidden;
        transition: max-height 1s ease-in-out;
      }}
    </style>
  </head>
  <body>
    <center>
      <button class="accordion">Main settings</button>
      <div class="panel">
        <center>
          <h1>Asetukset</h1>
        </center>
        <form action="./" method="GET">
          <center>
            <div>
              <label for="limit"
                >Valitse raja-arvo, jonka yli palaa punainen valo</label
              >
              <select name="limit" value="" id="limit">
                <option value="0">Päivän keskiarvo</option>
                <option value="5">5snt</option>
                <option value="10">10snt</option>
                <option value="15">15snt</option>
                <option value="20">20snt</option>
                <option value="25">25snt</option>
                <option value="30">30snt</option>
              </select>
            </div>
            <div>
              <button type="submit">Tallenna</button>
            </div>
          </center>
        </form>
        <br />
        <hr />
        <form action="./" method="GET">
          <center>
            <div>
              <label for="rounding"
                >Valitse pyöristetäänkö näytöllä olevat luvut kokonaisiin
                sentteihin</label
              >
              <select name="rounding" value="" id="rounding">
                <option value="1">Kyllä</option>
                <option value="0">Ei</option>
              </select>
            </div>
            <div>
              <button type="submit">Tallenna</button>
            </div>
          </center>
        </form>
        <br />
        <hr />
        <form action="./" method="GET">
          <center>
            <div>
              <label for="otaupdates">Automaattiset päivitykset</label>
              <select name="otaupdates" value="" id="otaupdates">
                <option value="1">Kyllä</option>
                <option value="0">Ei</option>
              </select>
            </div>
            <div>
              <button type="submit">Tallenna</button>
            </div>
          </center>
        </form>
        <br />
        <hr />
        <form action="./" method="GET">
          <center>
            <div>
              <label>Päivitä laite nyt</label>
            </div>
            <div>
              <button type="submit" name="updatenow" value="true">
                Tallenna
              </button>
            </div>
          </center>
        </form>
      </div>
    </center>
    <center>
      <button class="accordion">Wifi settings</button>
      <div class="panel">
        <center><h1>Wifi settings</h1></center>
        <form action="./" method="GET">
          <center>
            <div>
              <label for="ssid">SSID</label>
              <input type="text" name="ssid" id="ssid" value="" />
            </div>
            <div>
              <label for="to">Password</label>
              <input type="text" name="password" id="password" value="" />
            </div>
            <div>
              <button type="submit">Save and restart</button>
            </div>
          </center>
        </form>
      </div>
    </center>
    <center>
        <button class="accordion">Device info</button>
        <div class="panel">
          <center><h1>Device info</h1></center>
          <p>Software version: {version}</p>
        </div>
      </center>
    <script>
      var acc = document.querySelectorAll(".accordion");

      // Iterate to add event listeners
      acc.forEach((item) => {{
        item.addEventListener("click", function () {{
          // When it's clicked, loop through all the items
          acc.forEach((el) => {{
            // Close any open items
            if (el.classList.contains("active")) {{
              closeAcc(el);
              // If it's the one that was clicked and it's closed, open it
            }} else if (el === item) {{
              openAcc(el);
            }}
          }});
        }});
      }});

      function closeAcc(el) {{
        el.classList.remove("active");
        el.nextElementSibling.style.maxHeight = null;
      }}

      function openAcc(el) {{
        el.classList.add("active");
        el.nextElementSibling.style.maxHeight =
          el.nextElementSibling.scrollHeight + "px";
      }}
    </script>
  </body>
</html>



        """
    return str(html)
