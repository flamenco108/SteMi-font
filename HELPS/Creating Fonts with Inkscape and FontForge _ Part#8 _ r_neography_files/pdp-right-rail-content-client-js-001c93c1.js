import{c as t,_ as e,s,x as a,e as i,a as l,v as o,u as r,n as c,a$ as n,b0 as d,w as p}from"./shell-6eeab4aa.js";import{e as b,n as u}from"./ref-e092bf43.js";import"./icon-caret-right-f102b129.js";import"./faceplate-tabgroup-8ab8c427.js";import"./faceplate-tabpanel-ee186453.js";import"./faceplate-tablist-4fa130b8.js";import"./pageable-832f4cce.js";import"./icon-caret-right-outline-e46aff48.js";var h;const m=["global/view/discovery_unit","right_rail/click/panel_tab","right_rail/view/panel_tab","post/view/post","post/consume/post","post/click/post","post/click/subreddit","post/click/comments"];let v=h=class extends s{constructor(){super(),this.tabPanelsRef=b(),this.tabSelectCallback=t=>{for(const e of t)if("attributes"===e.type&&"faceplate-tab-selected"===e.attributeName&&e.target.nodeType===Node.ELEMENT_NODE){e.target.hasAttribute("faceplate-tab-selected")&&this.handleTabSelect(e.target)}},this.tabSelectObserver=new MutationObserver(this.tabSelectCallback),this.handlePDPRightRailTelemetry=t=>{const e=t.detail.details||t.detail;if(s=e,!m.includes(l(s)))return;var s;let a;try{const e=t?.target,s=e?.closest("span[event-data]")?.getAttribute("event-data")??e?.closest("reddit-pdp-right-rail-post")?.getAttribute("event-data");a=s?JSON.parse(decodeURIComponent(s)):{}}catch{a={}}e.action_info={...e.action_info,...a.action_info,type:"right_rail"},"post"===e.source&&(e.post=a.post||{},e.subreddit=a.subreddit||{})},this.handleTabSelect=t=>{const e=t.slot;e&&this.querySelector(`[slot="tab-panel"] [slot="${e}"] faceplate-partial[loading="programmatic"]`)?.load()},this.handleButtonClick=t=>{t.preventDefault()},this.addEventListener("faceplate-track",this.handlePDPRightRailTelemetry),this.addEventListener("track-event",this.handlePDPRightRailTelemetry)}firstUpdated(){this.querySelector('[slot="tabs"]')?.addEventListener("click",this.handleButtonClick)}connectedCallback(){super.connectedCallback(),this.tabSelectObserver.observe(this,h.tabSelectObserverOptions)}disconnectedCallback(){super.disconnectedCallback(),this.tabSelectObserver.disconnect(),this.querySelector('[slot="tabs"]')?.removeEventListener?.("click",this.handleButtonClick)}render(){return a`\n <div>\n <slot name="tabs" class="block sticky z-1 top-0 bg-neutral-background"></slot>\n <div ${u(this.tabPanelsRef)} class="pt-sm pb-lg">\n <slot name="tab-panel"></slot>\n </div>\n </div>\n `}};v.styles=[t],v.tabSelectObserverOptions={childList:!0,subtree:!0,attributes:!0,attributeFilter:["faceplate-tab-selected"]},v=h=e([i("pdp-right-rail")],v);const g=o(r(s));let k=class extends g{constructor(){super(...arguments),this.postId="",this.consumeTimeoutId=null,this._outboundLinkTrackingController=new n(this,(()=>({pageType:d(),postId:this.postId})))}connectedCallback(){super.connectedCallback(),this.enableObserver()}disconnectedCallback(){super.disconnectedCallback(),this.disableObserver(),this.clearConsumeTimeout()}clearConsumeTimeout(){this.consumeTimeoutId&&(clearTimeout(this.consumeTimeoutId),this.consumeTimeoutId=null)}observerIsIntersectingCallback(){this.consumeTimeoutId=setTimeout((()=>{this.trackEvent(p({source:"post",action:"consume",noun:"post"}))}),2e3)}observerIsNotIntersectingCallback(){this.clearConsumeTimeout()}createRenderRoot(){return this}};e([c({type:String,attribute:"post-id"})],k.prototype,"postId",void 0),k=e([i("reddit-pdp-right-rail-post")],k);
//# sourceMappingURL=pdp-right-rail-content-client-js-001c93c1.js.map
