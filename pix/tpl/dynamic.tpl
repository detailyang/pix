<style>
body {
    margin: 0px;
}
.art {
    position: relative;
    width: {{ width }}px;
    height: {{ width }}px;
    animation: {{duration}}s art steps(1) infinite;
}

@keyframes art {
   {% for k in keyframes %}
        {{k.progress}} {
            box-shadow: {{k.frame}};
        }
   {% endfor %}
}
</style>

<div class="art"></div>
