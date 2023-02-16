/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {browser} from "@web/core/browser/browser";

const {Component} = owl;

export class YoutubeMenu extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.user = useService("user");
        const {origin} = browser.location;
        const {userId} = this.user;
        this.source = `${origin}/web/image?model=res.users&field=avatar_128&id=${userId}`;
    }

    async onClick() {
        var vars = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('#') + 1).split('&');
        for (var i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            vars.push(hash[0]);
            vars[hash[0]] = hash[1];
        } ;
        const params = vars;
        const db_version = await this.rpc('/help/version', {});
        $.ajax({
            type: "POST",
            url: "https://dev.ineco.co.th/youtube",
            crossDomain: true,
            data: JSON.stringify({
                version: "16.0",
                model: params["model"],
                viewtype: params['view_type'],
                uuid: db_version['version']
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                var url;
                if (data) {
                    $.each(data, function (i, item) {
                        url = data[i];
                    });
                    if (url.length > 0) {
                        browser.open(url, "_blank");
                    } else {
                        alert('ไม่พบวิธีการใช้งาน');
                    };
                }
            },
            error: function (errMsg) {
                alert('ไม่พบวีดีโอที่ต้องการ');
            }
        });
    }

}

YoutubeMenu.template = "ineco_help_v16.YoutubeMenu";
YoutubeMenu.props = {
    onSelected: {
        type: Function,
        optional: true,
    }
}

export const systrayItem = {
    Component: YoutubeMenu,
};
registry.category("systray").add("ineco_help_v16.youtube_menu", systrayItem, {sequence: 10});
