import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

function getWidget(node, name) {
    return node.widgets?.find(w => w.name === name);
}

function getParams(node) {
    const params = {};
    if (!node.widgets) return params;
    for (const w of node.widgets) {
        if (w.name) params[w.name] = w.value;
    }
    return params;
}

function toast(msg, color = "#333") {
    const el = document.createElement("div");
    el.textContent = msg;
    Object.assign(el.style, {
        position: "fixed", bottom: "30px", right: "30px",
        background: color, color: "#fff",
        padding: "8px 16px", borderRadius: "8px",
        fontSize: "13px", zIndex: "9999",
        boxShadow: "0 2px 8px rgba(0,0,0,.4)",
        transition: "opacity .5s",
    });
    document.body.appendChild(el);
    setTimeout(() => { 
        el.style.opacity = "0"; 
        setTimeout(() => el.remove(), 600); 
    }, 3000);
}

function styledBtn(label, title, color = "#3a7bd5") {
    const btn = document.createElement("button");
    btn.textContent = label;
    btn.title = title;
    Object.assign(btn.style, {
        padding: "4px 10px", margin: "2px",
        borderRadius: "5px", border: "none",
        background: color, color: "#fff",
        cursor: "pointer", fontSize: "12px",
        fontWeight: "bold", lineHeight: "1.4",
        whiteSpace: "nowrap",
        transition: "background 0.2s"
    });
    btn.onmouseover = () => btn.style.background = shadeColor(color, -20);
    btn.onmouseout = () => btn.style.background = color;
    return btn;
}

function shadeColor(color, percent) {
    let R = parseInt(color.substring(1,3),16);
    let G = parseInt(color.substring(3,5),16);
    let B = parseInt(color.substring(5,7),16);
    R = (R<255)?R:255;  
    G = (G<255)?G:255;  
    B = (B<255)?B:255;  
    return "#" + ((R * (100 + percent) / 100) | 0).toString(16).padStart(2, '0') +
           ((G * (100 + percent) / 100) | 0).toString(16).padStart(2, '0') +
           ((B * (100 + percent) / 100) | 0).toString(16).padStart(2, '0');
}

app.registerExtension({
    name: "ComfyUI.PromptPresets.UI",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "PromptPresetsNode") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            if (onNodeCreated) onNodeCreated.apply(this, arguments);
            const node = this;

            const handlePreset = async (action, type) => {
                const params = getParams(node);
                const targetWidgetName = type === "characters" ? "character_preset" : "prompt_preset";
                const targetWidget = getWidget(node, targetWidgetName);
                
                let name = params.new_preset_name || "";
                const value = params.new_preset_value || "";

                if (action === "delete") {
                    name = targetWidget?.value;
                    if (!name || name === "None") {
                        toast("Select a valid item to delete.", "#f57c00");
                        return;
                    }
                }

                if (action === "add") {
                    if (!name || !name.trim()) {
                        toast("Fill 'new_preset_name' before adding.", "#f57c00");
                        return;
                    }
                }

                try {
                    const resp = await api.fetchApi("/prompt_presets/manage", { 
                        method: "POST", 
                        body: JSON.stringify({ 
                            action, 
                            config_path: params.config_path, 
                            type, 
                            name: name.trim(), 
                            value 
                        }) 
                    });
                    
                    const data = await resp.json();
                    
                    if (data.status === "success" && targetWidget) {
                        targetWidget.options.values = ["None", ...data.keys];
                        
                        if (action === "add") {
                            targetWidget.value = name.trim();
                            const nameWidget = getWidget(node, "new_preset_name");
                            const valueWidget = getWidget(node, "new_preset_value");
                            if (nameWidget) nameWidget.value = "";
                            if (valueWidget) valueWidget.value = "";
                            toast(`Added: ${name}`, "#2e7d32");
                        } else {
                            targetWidget.value = "None";
                            toast(`Deleted: ${name}`, "#c62828");
                        }
                        node.setDirtyCanvas(true, true);
                    } else {
                        toast("Operation failed.", "#b71c1c");
                    }
                } catch (e) {
                    toast(`${e.message || e}`, "#b71c1c");
                }
            };

            const bar = document.createElement("div");
            Object.assign(bar.style, {
                display: "flex", flexWrap: "nowrap", padding: "4px 6px", 
                gap: "2px", width: "max-content", minWidth: "100%",
                justifyContent: "center"
            });

            const addAction = (label, title, color, actionFn) => {
                const btn = styledBtn(label, title, color);
                btn.addEventListener("click", async () => {
                    btn.disabled = true; 
                    btn.style.opacity = "0.5";
                    try { await actionFn(); } 
                    catch (e) { 
                        toast(`${e.message || e}`, "#b71c1c"); 
                    }
                    finally { 
                        btn.disabled = false; 
                        btn.style.opacity = "1"; 
                    }
                });
                bar.appendChild(btn);
            };

            addAction("Add Char", "Add Character", "#2e7d32", () => handlePreset("add", "characters"));
            addAction("Del Char", "Delete Character", "#c62828", () => handlePreset("delete", "characters"));

            const divider = document.createElement("div");
            divider.style.width = "1px";
            divider.style.background = "#444";
            divider.style.margin = "2px 4px";
            bar.appendChild(divider);

            addAction("Add Prompt", "Add Prompt", "#3a7bd5", () => handlePreset("add", "prompts"));
            addAction("Del Prompt", "Delete Prompt", "#c62828", () => handlePreset("delete", "prompts"));

            node.addDOMWidget("prompt_presets_controls", "btn_bar", bar, {
                serialize: false,
                hideOnZoom: false,
            });
        };
    }
});
