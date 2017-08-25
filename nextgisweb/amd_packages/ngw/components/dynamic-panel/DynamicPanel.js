define([
    "dojo/Evented",
    'dojo/_base/declare',
    'ngw-pyramid/i18n!webmap',
    'ngw-pyramid/hbs-i18n',
    "dojo/query",
    "dojo/_base/lang",
    "dojo/_base/array",
    "dojo/dom",
    "dojo/dom-construct",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dijit/layout/ContentPane",
    "dijit/layout/BorderContainer",
    "dojo/text!./DynamicPanel.hbs",
    "dijit/layout/BorderContainer",
    "dijit/form/Select",
    "xstyle/css!./DynamicPanel.css"
], function (
    Evented,
    declare,
    i18n,
    hbsI18n,
    query,
    lang,
    array,
    dom,
    domConstruct,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    ContentPane,
    BorderContainer,
    template) {
    return declare([ContentPane,_TemplatedMixin, _WidgetsInTemplateMixin],{
        templateString: hbsI18n(template, i18n),
        title: "",
        component: [],
        isOpen: false,
        constructor: function (options) {
            declare.safeMixin(this,options);
        },
        postCreate(){
            this.component.placeAt(this.contentNode);
            if (this.isOpen) this.show();

            query(this.closer).on("click", lang.hitch(this, function() {
               this.hide();
            }));
        },
        show(){
            this.isOpen = true;
            this.containerNode.style.display = "block";
            if (this.getParent()) this.getParent().resize();
            this.emit("shown");
        },
        hide(){
            this.isOpen = false;
            this.containerNode.style.display = "none";
            if (this.getParent()) this.getParent().resize();
            this.emit("closed");
        }
    });
});