// Generated by CoffeeScript 1.3.3
(function() {
  var Main,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  Main = (function() {

    Main.prototype.drawBones = function(data) {
      var joint, x, _i, _len, _ref, _results;
      _ref = data.bones;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        x = _ref[_i];
        if (x['hand_left']['x'] !== 0) {
          _results.push((function() {
            var _results1;
            _results1 = [];
            for (joint in x) {
              this.ctx.beginPath();
              this.ctx.arc(500 + (x[joint]['x'] * 500), 200 + -x[joint]['y'] * 500, 40, 0, 2 * Math.PI);
              _results1.push(this.ctx.stroke());
            }
            return _results1;
          }).call(this));
        } else {
          _results.push(void 0);
        }
      }
      return _results;
    };

    Main.prototype.deviceReady = function(data) {
      var image_data, img,
        _this = this;
      this.getJoints();
      if (data.rgb) {
        image_data = 'data:image/jpg;base64,' + data.rgb;
        img = new Image();
        img.onload = function() {
          _this.ctx.clearRect(0, 0, 1024, 768);
          _this.ctx.drawImage(img, 0, 0, 1024, 768);
          return _this.drawBones(data);
        };
        return img.src = image_data;
      } else {
        this.ctx.clearRect(0, 0, 1024, 768);
        return this.drawBones(data);
      }
    };

    Main.prototype.getJoints = function() {
      return $.ajax({
        url: 'http://localhost:8080',
        dataType: 'jsonp',
        jsonpCallback: 'jsonCallback',
        jsonp: 'callback'
      });
    };

    function Main() {
      this.getJoints = __bind(this.getJoints, this);

      this.deviceReady = __bind(this.deviceReady, this);

      this.drawBones = __bind(this.drawBones, this);
      this.can = $("canvas")[0];
      this.can.width = 1024;
      this.can.height = 768;
      this.ctx = this.can.getContext("2d");
      window.jsonCallback = this.deviceReady;
      this.getJoints();
    }

    return Main;

  })();

  $(document).ready(function() {
    return new Main();
  });

}).call(this);