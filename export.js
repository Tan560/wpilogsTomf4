const HELP_URL = "https://github.com/Mechanical-Advantage/AdvantageScope/blob/main/docs/EXPORT.md#options";
const FORMAT = document.getElementById("format");
const SAMPLING_MODE = document.getElementById("samplingMode");
const SAMPLING_MODE_AKIT = SAMPLING_MODE.children[2];
const SAMPLING_PERIOD = document.getElementById("samplingPeriod");
const PREFIXES = document.getElementById("prefixes");
const INCLUDE_GENERATED = document.getElementById("includeGenerated");
const EXIT_BUTTON = document.getElementById("exit");
const CONFIRM_BUTTON = document.getElementById("confirm");
const HELP_BUTTON = document.getElementsByClassName("help-div")[0].firstElementChild;
window.addEventListener("message", (event) => {
    if (event.source === window && event.data === "port") {
        let messagePort = event.ports[0];
        messagePort.onmessage = (event) => {
            if (typeof event.data === "object") {
                if ("isFocused" in event.data) {
                    Array.from(document.getElementsByTagName("button")).forEach((button) => {
                        if (event.data.isFocused) {
                            button.classList.remove("blurred");
                        }
                        else {
                            button.classList.add("blurred");
                        }
                    });
                }
                if ("supportsAkit" in event.data) {
                    let supportsAkit = event.data.supportsAkit;
                    SAMPLING_MODE_AKIT.disabled = !supportsAkit;
                }
            }
        };
        function confirm() {
            let format = "csv-table";
            if (FORMAT.value === "csv-table")
                format = "csv-table";
            if (FORMAT.value === "csv-list")
                format = "csv-list";
            if (FORMAT.value === "wpilog")
                format = "wpilog";
            if (FORMAT.value === "mcap")
                format = "mcap";
            let samplingMode = "changes";
            if (SAMPLING_MODE.value === "changes")
                samplingMode = "changes";
            if (SAMPLING_MODE.value === "fixed")
                samplingMode = "fixed";
            if (SAMPLING_MODE.value === "akit")
                samplingMode = "akit";
            let options = {
                format: format,
                samplingMode: samplingMode,
                samplingPeriod: Number(SAMPLING_PERIOD.value),
                prefixes: PREFIXES.value,
                includeGenerated: INCLUDE_GENERATED.value === "true"
            };
            messagePort.postMessage(options);
        }
        let updateDisabled = () => {
            SAMPLING_PERIOD.disabled = SAMPLING_MODE.value !== "fixed";
        };
        SAMPLING_MODE.addEventListener("change", updateDisabled);
        updateDisabled();
        SAMPLING_PERIOD.addEventListener("change", () => {
            if (Number(SAMPLING_PERIOD.value) <= 0) {
                SAMPLING_PERIOD.value = "1";
            }
        });
        EXIT_BUTTON.addEventListener("click", () => {
            messagePort.postMessage(null);
        });
        CONFIRM_BUTTON.addEventListener("click", confirm);
        window.addEventListener("keydown", (event) => {
            if (event.code === "Enter")
                confirm();
        });
        HELP_BUTTON.addEventListener("click", () => {
            messagePort.postMessage(HELP_URL);
        });
    }
});
