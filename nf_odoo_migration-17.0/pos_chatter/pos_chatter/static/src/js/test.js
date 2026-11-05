odoo.define("rating.portal.chatter", function (require) {
    "use strict";

    var core = require("web.core");
    var portalChatter = require("portal.chatter");
    var utils = require("web.utils");
    var time = require("web.time");
    const dom = require("web.dom");
    const ajax = require("web.ajax");
    var publicWidget = require("web.public.widget");
    var portalComposer = require("portal.composer");
    const { Markup } = require("web.utils");
    var _t = core._t;

    var PortalChatter = portalChatter.PortalChatter;
    var QWeb = core.qweb;

    PortalChatter.include({
        events: _.extend({}, PortalChatter.prototype.events, {
            "click .close_card": "close_window",
            "click #button_send": "_onClickMessageSend",
            "click .pos-message": "_nf_click_systra",
            "click .pos-filter": "on_click_filter",
            "click .o_mail_channel_preview": "on_click_message_item",
            "click .pos-new_message": "on_click_new_message",
        }),
       
        _nf_click_systra: function () {
            var self = this;
            // $('.o_mail_navbar_dropdown_channels').html(QWeb.render('Spinner'));
            console.log("123 --> ", $(".o_mail_navbar_dropdown_channels"));
        },
        on_click_filter: async function () {
            let channel_id = 1;
            var self = this;
            await ajax
                .jsonRpc("/pos_systray/chat_message", "call", {
                    data: "5",
                })
                .then(async function (result) {
                    let state = { name: {}, data: {}, id: {} };
                    if (self.flag_scroll == 1) {
                        var element =
                            this.root.el.querySelector("#msg_content");
                        element.scrollTop = element.scrollHeight;
                    }
                    var message_list = [];
                    var messages = result.messages;
                    $(messages).each(function (message) {
                        const htmlString = messages[message].body;
                        const parser = new DOMParser();
                        const parsedHtml = parser.parseFromString(
                            htmlString,
                            "text/html"
                        );
                        const plainText =
                            parsedHtml.documentElement.textContent;
                        message_list.push({
                            body: plainText,
                            author: messages[message].author,
                            flag: messages[message].flag,
                        });
                    });
                    state.data = message_list;
                    state.name = result.name;
                    state.id = result.channel_id;
                    var template1 = await QWeb.render("ChatMsgView", {
                        props: {
                            channel_id: 5,
                        },
                        state,
                    });
                    $(".o_mail_navbar_dropdown_channels").html(template1);
                });
        },
        close_window: function (ev) {
            $(".o_mail_navbar_dropdown_channels").empty()
        },
        _onClickMessageSend() {
            var self = this
            var input_value = $("#message_to_send")
            var res_id = $("#button_send").attr("value")
            var element = $("#msg_content");
            element.scrollTop = element.scrollHeight;
            console.log('>>>>>>>>>>', input_value);
            if (input_value.val()) {
                var data = {
                    'res_id': res_id,
                    'msg_body': input_value.val()
                }
                console.log('data',data);
                ajax.jsonRpc('/pos_chatter/send_message', 'call', {
                    'data': data
                }).then(function() {
                    input_value.value = ""
                    self.on_click_filter()
                    // var res_id = self.root.el.querySelector("#button_send").getAttribute("value")
                    // self.render_messages();
                    // var element = self.root.el.querySelector("#msg_content");
                    // element.scrollTop = element.scrollHeight;
                })
            }
        }
    });
});
