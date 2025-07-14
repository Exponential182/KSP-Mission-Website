[1mdiff --git a/app.py b/app.py[m
[1mindex 1aee081..71c4d71 100644[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@ -27,11 +27,18 @@[m [mdef missions():[m
                             data=results)[m
 [m
 [m
[31m-# @app.route("/mission/<id:int>")[m
[31m-# def mission():[m
[31m-#     conn = sqlite3.connect(database)[m
[31m-#     cursor = conn.cursor()[m
[31m-#     return render_template("mission.html", data = results)[m
[32m+[m[32m@app.route("/mission/<int:id>")[m
[32m+[m[32mdef mission(id):[m
[32m+[m[32m    conn = sqlite3.connect(database)[m
[32m+[m[32m    cursor = conn.cursor()[m
[32m+[m[32m    query = f"SELECT * FROM Mission WHERE id = {id}"[m
[32m+[m[32m    cursor.execute(query)[m
[32m+[m[32m    results = cursor.fetchone()[m
[32m+[m[32m    results = list(results)[m
[32m+[m[32m    debug_res = [(index, val) for index, val in enumerate(results)][m
[32m+[m[32m    print(debug_res)[m
[32m+[m
[32m+[m[32m    return render_template("mission.html", title = "KSP Mission Library", data = results)[m
 [m
 [m
 @app.route("/engines")[m
[1mdiff --git a/static/css/style.css b/static/css/style.css[m
[1mindex 43448a9..3e61626 100644[m
[1m--- a/static/css/style.css[m
[1m+++ b/static/css/style.css[m
[36m@@ -221,4 +221,11 @@[m [mh1, h2, h3, h4, h5, h6{[m
 [m
 .info-card.wide-image{[m
     width: 20vw;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m/* Mission Specific Page (Maybe all Specific Pages) */[m
[32m+[m[32m.unbal-three-column-grid{[m
[32m+[m[32m    margin: 2vw;[m
[32m+[m[32m    display: grid;[m
[32m+[m[32m    grid-template-columns: 1fr 2fr 1fr;[m
 }[m
\ No newline at end of file[m
[1mdiff --git a/static/scripts/aspect_ratio_hander.js b/static/scripts/aspect_ratio_hander.js[m
[1mindex 389ed70..820d6e9 100644[m
[1m--- a/static/scripts/aspect_ratio_hander.js[m
[1m+++ b/static/scripts/aspect_ratio_hander.js[m
[36m@@ -6,6 +6,7 @@[m [mdocument.addEventListener("DOMContentLoaded", function () {[m
         if (!container) return;[m
 [m
         const applyAspectClass = () => {[m
[32m+[m[32m            // Calculate image aspect ratio and assign a class based on it.[m[41m [m
             const aspectRatio = img.naturalWidth / img.naturalHeight;[m
             container.classList.add(aspectRatio > 0.7 ? "wide-image" : "tall-image");[m
         };[m
[1mdiff --git a/templates/404.html b/templates/404.html[m
[1mindex 8c8e793..63cd33a 100644[m
[1m--- a/templates/404.html[m
[1m+++ b/templates/404.html[m
[36m@@ -9,8 +9,8 @@[m
 <body>[m
     <h1>404 Page Not Found</h1>[m
     <div>[m
[31m-        <p>The url you requested did not exist on the server.</p>[m
[31m-        <p>The url you attempted to go to was {{url}}</p>[m
[32m+[m[32m        <h3>The url does not exist.</h3>[m
[32m+[m[32m        <p>URL: <strong>{{url}}</strong></p>[m
     </div>[m
     <div>[m
          <img src="/static/images/decorative-images/Mars-spacecraft.png" alt="A Spacecraft over Mars">[m
[1mdiff --git a/templates/engines.html b/templates/engines.html[m
[1mindex 99fd2bc..3f2e6bb 100644[m
[1m--- a/templates/engines.html[m
[1m+++ b/templates/engines.html[m
[36m@@ -20,7 +20,7 @@[m
                     <br>[m
                     <h3>Ignitions: <br> {{i[5]}}</h3>[m
                     <br>[m
[31m-                    <a href="/stage/{{i[7]}}">More Details</a>[m
[32m+[m[32m                    <a href="/engine/{{i[7]}}">More Details</a>[m
                 </div>[m
             </div>[m
         {%endfor%}[m
[1mdiff --git a/templates/layout.html b/templates/layout.html[m
[1mindex e4a9133..772c945 100644[m
[1m--- a/templates/layout.html[m
[1m+++ b/templates/layout.html[m
[36m@@ -3,7 +3,7 @@[m
 <head>[m
     <meta charset="UTF-8">[m
     <meta name="viewport" content="width=device-width, initial-scale=1.0">[m
[31m-    <link rel="stylesheet" href="./static/css/style.css">[m
[32m+[m[32m    <link rel="stylesheet" href="{{url_for('static', filename='css/style.css')}}">[m
     <title>{{title}}</title>[m
 </head>[m
 <body>[m
