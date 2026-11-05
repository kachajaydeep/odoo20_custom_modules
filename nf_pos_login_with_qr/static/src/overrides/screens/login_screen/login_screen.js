import { _t } from "@web/core/l10n/translation";
import { LoginScreen } from "@point_of_sale/app/screens/login_screen/login_screen";
import { patch } from "@web/core/utils/patch";
import { onWillUnmount, useExternalListener, proxy } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

patch(LoginScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.nf_qr_state = proxy({
            'qr_scan' : false
        })
        this.notification = useService("notification");
    },

    clickBack() {
        this.nf_qr_state.qr_scan = false;
        clearInterval(this.nfQrInterval);
        const video = document.getElementById("video");
        this.stopVideoStream(video);
        super.clickBack();
    },

    async onClickScanQR(ev) {
        let self = this;
        this.nf_qr_state.qr_scan = true;
        const video = ev.target.offsetParent.querySelector('#video');
        let cam_stream;
        try{
           cam_stream = await  navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        }
        catch(error){
            console.error("Unable to access Camera:",error);
            this.nf_qr_state.qr_scan = false;

            if(error.name === "NotAllowedError"){
                this.notification.add(
                    _t("No camera was found on this device."),
                     { type: "warning" },
                    5000
                )
            }
            else if(error.name === "NotFoundError"){
                this.notification.add(
                    _t("No camera was found on this device."),
                    { type: "danger" },
                    5000
                )
            } else {
            this.notification.add(
                _t("Unable to access the camera."),
                { type: "danger" },
                5000
            );
        }


            return
        }
        video.srcObject = cam_stream;
        video.addEventListener('loadedmetadata', (event) => {
            video.width = video.videoWidth;
            video.height = video.videoHeight;
        });
        video.addEventListener('canplay', () => {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = video.width;
            canvas.height = video.height;
            this.nfQrInterval = setInterval(() => {
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
                const code = jsQR(imageData.data, imageData.width, imageData.height);
                if (code) {
                    let pin = code.data;
                    const allEmployees = self.pos.models["hr.employee"].filter(
                        (employee) => employee.id !== self.pos.getCashier()?.id
                    );
                    const pinMatchEmployees = allEmployees.filter(
                        (employee) => !pin || pin === employee._pin
                    );
                    if (pinMatchEmployees.length >= 1) {
                        self.nf_qr_state.qr_scan = false;
                        self.selectOneCashier(pinMatchEmployees[0]);
                        self.notification.add(_t("Login Successful!!!"), { type: "success" }, 3000);
                        clearInterval(self.nfQrInterval);
                        setTimeout(() => {
                            self.stopVideoStream(video)
                        }, 500);
                    } else {
                        self.notification.add(_t("QR Not found!!!"), { type: "danger" }, 3000);
//                        clearInterval(self.nfQrInterval);
//                        setTimeout(() => {
//                            self.stopVideoStream(video)
//                        }, 500);
                    }
                }
            }, 1000);
        });
    },

    stopVideoStream(video) {
        const stream = video.srcObject;
        if (stream) {
          const tracks = stream.getTracks();
          tracks.forEach(track => track.stop()); // Stop all video tracks
          video.srcObject = null; // Set the video source to null to stop playback
        }
    }

});
