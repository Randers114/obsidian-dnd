'use strict';

var obsidian = require('obsidian');

/*! *****************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */
/* global Reflect, Promise */

var extendStatics = function(d, b) {
    extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
    return extendStatics(d, b);
};

function __extends(d, b) {
    extendStatics(d, b);
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
}

function __awaiter(thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
}

function __generator(thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
}

function __values(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
}

var CompletedAreaSettingTab = /** @class */ (function (_super) {
    __extends(CompletedAreaSettingTab, _super);
    function CompletedAreaSettingTab(app, plugin) {
        var _this = _super.call(this, app, plugin) || this;
        _this.defaultHeaderLevel = "2";
        _this.defaultHeaderName = "Completed";
        _this.plugin = plugin;
        return _this;
    }
    CompletedAreaSettingTab.prototype.display = function () {
        var _this = this;
        var containerEl = this.containerEl;
        containerEl.empty();
        new obsidian.Setting(containerEl)
            .setName("Header level")
            .setDesc("number of `#`s in the header.")
            .addText(function (text) {
            return text
                .setPlaceholder(_this.defaultHeaderLevel)
                .setValue(_this.plugin.setting.completedAreaHierarchy)
                .onChange(function (value) {
                if (_this.isHierarchyValid(value)) {
                    _this.plugin.setting.completedAreaHierarchy =
                        value || _this.defaultHeaderLevel;
                    _this.plugin.saveData(_this.plugin.setting).then(function () {
                        text.setValue(value);
                    });
                }
                else {
                    new obsidian.Notice("Header level's number not valid!");
                }
            });
        });
        new obsidian.Setting(containerEl)
            .setName("Header name")
            .setDesc("where the completed items be extracted to.")
            .addText(function (text) {
            return text
                .setPlaceholder(_this.defaultHeaderName)
                .setValue(_this.plugin.setting.completedAreaName)
                .onChange(function (value) {
                _this.plugin.setting.completedAreaName =
                    value || _this.defaultHeaderName;
                _this.plugin.saveData(_this.plugin.setting);
                text.setValue(value);
            });
        });
        new obsidian.Setting(containerEl)
            .setName("Show icon on left sidebar")
            .addToggle(function (toggle) {
            toggle.setValue(_this.plugin.setting.showIcon).onChange(function (value) {
                _this.plugin.setting.showIcon = value;
                _this.plugin.saveData(_this.plugin.setting);
                new obsidian.Notice("Reload the app to see icon " + (value ? "added" : "removed") + ".");
            });
        });
    };
    CompletedAreaSettingTab.prototype.isHierarchyValid = function (hierarchyLevel) {
        var e_1, _a;
        var validLevels = [1, 2, 3, 4, 5, 6];
        try {
            for (var validLevels_1 = __values(validLevels), validLevels_1_1 = validLevels_1.next(); !validLevels_1_1.done; validLevels_1_1 = validLevels_1.next()) {
                var validNum = validLevels_1_1.value;
                if (Number(hierarchyLevel) === validNum || hierarchyLevel === "") {
                    return true;
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (validLevels_1_1 && !validLevels_1_1.done && (_a = validLevels_1.return)) _a.call(validLevels_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return false;
    };
    return CompletedAreaSettingTab;
}(obsidian.PluginSettingTab));

var CompletedAreaSetting = /** @class */ (function () {
    function CompletedAreaSetting() {
        this.completedAreaHierarchy = "2";
        this.completedAreaName = "Completed";
        this.todoAreaName = "Todo";
        this.showIcon = true;
        this.sortedBy = "Asc";
    }
    return CompletedAreaSetting;
}());

obsidian.addIcon("completed-area", '<g id="icon" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><rect id="Rectangle" stroke="currentColor" stroke-width="8" x="20" y="20" width="60" height="60" rx="10"></rect><path d="M68.7153857,33.5033079 L72.0903697,35.8858648 C72.5415551,36.2043773 72.6491076,36.8283407 72.3305951,37.2795261 L72.2641586,37.3636708 L48.720426,64.1010398 C46.5305195,66.5880005 42.7391695,66.8288105 40.2522088,64.638904 C40.1258491,64.5276373 40.0042287,64.4111011 39.8876706,64.2896051 L28.6056533,52.5296259 C28.258873,52.1681543 28.2330404,51.6058741 28.5452158,51.2141283 L31.9837559,46.899139 C32.3279438,46.467221 32.9571019,46.3961018 33.3890199,46.7402897 C33.4274056,46.7708786 33.4634871,46.8042521 33.4969719,46.8401396 L42.8381754,56.8516325 C43.5917202,57.6592488 44.8572913,57.7030825 45.6649076,56.9495377 L45.7632746,56.8511374 L67.4072774,33.6382921 C67.7482521,33.2726022 68.3069198,33.2149531 68.7153857,33.5033079 Z" id="Path" fill="currentColor" fill-rule="nonzero"></path></g>');
var CompletedAreaPlugin = /** @class */ (function (_super) {
    __extends(CompletedAreaPlugin, _super);
    function CompletedAreaPlugin() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.completedItemRegx = /(\n?- \[x\] .*)/g;
        return _this;
    }
    CompletedAreaPlugin.prototype.onload = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setting = new CompletedAreaSetting();
                        return [4 /*yield*/, this.loadSetting()];
                    case 1:
                        _a.sent();
                        if (this.setting.showIcon) {
                            this.addRibbonIcon("completed-area", "Completed Area", function () {
                                _this.editSource();
                            });
                        }
                        this.addCommand({
                            id: "completed-area-shortcut",
                            name: "Extracted completed items.",
                            hotkeys: [{ modifiers: ["Ctrl"], key: "Enter" }],
                            callback: function () {
                                _this.editSource();
                            },
                        });
                        this.addSettingTab(new CompletedAreaSettingTab(this.app, this));
                        return [2 /*return*/];
                }
            });
        });
    };
    CompletedAreaPlugin.prototype.loadSetting = function () {
        return __awaiter(this, void 0, void 0, function () {
            var loadedSetting;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.loadData()];
                    case 1:
                        loadedSetting = _a.sent();
                        if (loadedSetting) {
                            this.setting.completedAreaHierarchy =
                                loadedSetting.completedAreaHierarchy;
                            this.setting.completedAreaName = loadedSetting.completedAreaName;
                            this.setting.todoAreaName = loadedSetting.todoAreaName;
                            this.setting.showIcon = loadedSetting.showIcon;
                        }
                        else {
                            this.saveData(this.setting);
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    CompletedAreaPlugin.prototype.editSource = function () {
        var _a, _b;
        var activeLeaf = (_a = this.app.workspace.activeLeaf) !== null && _a !== void 0 ? _a : null;
        if (activeLeaf) {
            var source = activeLeaf.view.sourceMode;
            var sourceText = source.get();
            var todoRegx = /-\s\[[\sx]\]\s/gi;
            var toggledText = this.toggleElement(todoRegx, this.replaceTodo);
            var completedItems = (_b = this.extractCompletedItems(toggledText)) !== null && _b !== void 0 ? _b : null;
            if (completedItems) {
                var newText = this.refactorContent(toggledText, completedItems);
                source.set(newText, false);
            }
        }
        else {
            new obsidian.Notice("Please active a leaf first.");
        }
    };
    CompletedAreaPlugin.prototype.replaceTodo = function (startWith) {
        return startWith === "- [ ] " ? "- [x] " : "- [ ] ";
    };
    CompletedAreaPlugin.prototype.extractCompletedItems = function (text) {
        var completedItems = [];
        if (text) {
            completedItems = text.match(this.completedItemRegx);
            if (!completedItems) {
                new obsidian.Notice("No completed todos found.");
                return;
            }
            return completedItems;
        }
    };
    CompletedAreaPlugin.prototype.refactorContent = function (content, items) {
        var completedArea = this.formatItems(items, content);
        console.log(completedArea);
        var header = this.completedAreaHeader.trimStart();
        var newContent = content
            .replace(this.completedItemRegx, "") // Remove completed items in main text
            .trimStart()
            .trimEnd();
        return this.isCompletedAreaExisted(content)
            ? newContent.replace(header, "" + header + completedArea)
            : newContent + completedArea;
    };
    CompletedAreaPlugin.prototype.formatItems = function (items, content) {
        var completedArea = "";
        var header = this.makeCompletedHeader(content);
        items[0] = (items[0][0] === "\n" ? "" : "\n") + items[0];
        completedArea = items.reduce(function (prev, current) {
            return prev + current;
        }, header);
        return completedArea;
    };
    CompletedAreaPlugin.prototype.makeCompletedHeader = function (content) {
        this.completedAreaHeader =
            "\n" +
                "#".repeat(Number(this.setting.completedAreaHierarchy)) +
                (" " + this.setting.completedAreaName);
        return this.isCompletedAreaExisted(content)
            ? "" // if completed header already exists
            : this.completedAreaHeader;
    };
    CompletedAreaPlugin.prototype.isCompletedAreaExisted = function (content) {
        return !!content.match(RegExp(this.completedAreaHeader));
    };
    CompletedAreaPlugin.prototype.toggleElement = function (re, subst) {
        var activeLeaf = this.app.workspace.activeLeaf;
        var editor = activeLeaf.view.sourceMode.cmEditor;
        var selection = editor.somethingSelected();
        var selectedText = this.getSelectedText(editor);
        var newString = selectedText.content.replace(re, subst);
        editor.replaceRange(newString, selectedText.start, selectedText.end);
        // Keep cursor in the same place
        if (selection) {
            editor.setSelection(selectedText.start, {
                line: selectedText.end.line,
                ch: editor.getLine(selectedText.end.line).length,
            });
        }
        return activeLeaf.view.sourceMode.get();
    };
    CompletedAreaPlugin.prototype.getSelectedText = function (editor) {
        if (editor.somethingSelected()) {
            // Toggle to-dos under the selection
            var cursorStart = editor.getCursor(true);
            var cursorEnd = editor.getCursor(false);
            var content = editor.getRange({ line: cursorStart.line, ch: 0 }, { line: cursorEnd.line, ch: editor.getLine(cursorEnd.line).length });
            return {
                start: { line: cursorStart.line, ch: 0 },
                end: {
                    line: cursorEnd.line,
                    ch: editor.getLine(cursorEnd.line).length,
                },
                content: content,
            };
        }
        else {
            // Toggle the todo in the line
            var lineNr = editor.getCursor().line;
            var contents = editor.getDoc().getLine(lineNr);
            var cursorStart = {
                line: lineNr,
                ch: 0,
            };
            var cursorEnd = {
                line: lineNr,
                ch: contents.length,
            };
            var content = editor.getRange(cursorStart, cursorEnd);
            return { start: cursorStart, end: cursorEnd, content: content };
        }
    };
    return CompletedAreaPlugin;
}(obsidian.Plugin));

module.exports = CompletedAreaPlugin;


/* nosourcemap */