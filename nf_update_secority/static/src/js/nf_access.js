/* @odoo-module */
import {ActionMenus} from "@web/search/action_menus/action_menus";
import {patch} from "@web/core/utils/patch";
import { user } from "@web/core/user";
import { onWillStart } from "@odoo/owl";


patch(ActionMenus.prototype, {
    setup() {
        super.setup(...arguments);
    },
    async getActionItems(props) {
        let nf_group_no_archive = await user.hasGroup("nf_update_secority.nf_group_no_archive")
        let nf_group_no_duplicate = await user.hasGroup("nf_update_secority.nf_group_no_duplicate")
        let nf_group_no_delete = await user.hasGroup("nf_update_secority.nf_group_no_delete")

        var accessright_list = await super.getActionItems(props);
        if (accessright_list.length > 0) {
            
            return accessright_list.filter((action) => {
                if ( nf_group_no_archive && action.description == 'Archive') {
                    return false
                } else if (  nf_group_no_duplicate && action.description == 'Duplicate' ){
                    return false
                } else if (  nf_group_no_delete && action.description == "Delete" ){
                    return false
                } else{
                    return true
                }
            });
        }
        return accessright_list;
    },
});
