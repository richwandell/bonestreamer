class Main
     
     drawBones:(data)=>
          for x in data.bones
               if x['hand_left']['x'] != 0
                    for joint of x
                         @ctx.beginPath()
                         @ctx.arc( 500 + (x[joint]['x'] * 500), 200 + -x[joint]['y'] * 500 , 40, 0, 2*Math.PI )
                         @ctx.stroke()
     
     deviceReady: (data)=>
          @getJoints()
          @ctx.clearRect 0, 0, 1024, 768
          
          if data.rgb
               image_data = 'data:image/jpg;base64,'+data.rgb
               img = new Image()
               img.onload = =>
                    @ctx.drawImage(img, 0, 0, 1024, 768)
                    @drawBones(data)
               img.src = image_data
          else
               @drawBones(data)

     getJoints:=>
          $.ajax
               url: 'http://localhost:8080'
               dataType: 'jsonp'
               jsonpCallback: 'jsonCallback'
               jsonp: 'callback'
     
     constructor:->
          @can = $("canvas")[0]
          @can.width = 1024
          @can.height = 768
          @ctx = @can.getContext("2d")
          
          window.jsonCallback = @deviceReady

          @getJoints()


$(document).ready ->
     new Main()