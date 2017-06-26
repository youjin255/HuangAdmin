
// log
var log = function () {
    console.log(arguments);
};


// form
var formFromKeys = function(keys, prefix) {
    var form = {};
    for(var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var tagid = prefix + key;
        var value = $('#' + tagid).val();
        if (value.length < 1) {
            // alert('字段不能为空');
            break;
        }
        form[key] = value;
    }
    return form;
};

// vip API
var admin = {
  data:{}
};

admin.ajax = function(url, method, form, success, error) {
    var request = {
        url: url,
        type: method,
        contentType: 'application/json',
        success: function (r) {
            log('huang admin post success', url, r);
            success(r);
        },
        error: function (err) {
            var r = {
                success: false,
                data: err,
            };
            log('huang admin post err', url, err, error);
            error(r);
        }
    };
    if(method === 'post') {
        var data = JSON.stringify(form);
        request.data = data;
    }
    $.ajax(request);
};

admin.get = function(url, response) {
    var method = 'get';
    var form = {};
    this.ajax(url, method, form, response, response);
};

admin.post = function(url, form, success, error) {
    var method = 'post';
    this.ajax(url, method, form, success, error);
};

// API admin
admin.addBoard = function (form, success, error) {
    var url = '/admin/board/add';
    this.post(url, form, success, error);
};

admin.updatePermissions = function (form, success, error) {
    var url = '/admin/board/update';
    this.post(url, form, success, error);
};

// API normal
// vip.register = function(form, success, error) {
//     var url = '/auth/register';
//     this.post(url, form, success, error);
// };
//
// vip.login = function(form, success, error) {
//     var url = '/auth/login';
//     this.post(url, form, success, error);
// };
//
// // board API
// vip.board_all = function(response) {
//     var url = '/api/boards';
//     this.get(url, response);
// };
//
// vip.board = function(id, response) {
//     var url = '/api/boards/' + id;
//     this.get(url, response);
// };
//
// // topic API
// vip.topicsInBoard = function(board_id, response) {
//   var url = '/api/topics?board_id=' + board_id;
//   this.get(url, response);
// };
//
// vip.topic = function(id, response) {
//     var url = '/api/topics/' + id;
//     this.get(url, response);
// };
//
// // model with cache
// vip.model = function(type, id, response) {
//   // var key = type
// };
