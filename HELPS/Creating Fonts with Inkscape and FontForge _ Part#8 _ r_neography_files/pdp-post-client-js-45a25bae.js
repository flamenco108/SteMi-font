import{p as t,c as s,_ as e,n as o,s as r,r as a,x as i,e as d}from"./shell-6eeab4aa.js";import"./faceplate-progress-28a29127.js";import"./follow-button-44739e7a.js";const l=t(r),n=new DOMParser;let p=class extends l{constructor(){super(...arguments),this.postId="",this.onPostFlairChange=t=>{t.postId===this.postId&&this.renderUpdatedFlair(t.updatedHtml)}}connectedCallback(){super.connectedCallback(),this.subscribe(a.PostFlairUpdated,this.onPostFlairChange)}disconnectedCallback(){super.disconnectedCallback(),this.unsubscribe(a.PostFlairUpdated,this.onPostFlairChange)}renderUpdatedFlair(t){const s=this.shadowRoot?.querySelector("slot")?.assignedElements({flatten:!0})[0];if(!t&&s)return void s.remove();const e=n.parseFromString(t,"text/html").body.firstChild;e&&(s?s.replaceWith(e):this.appendChild(e))}render(){return i`<slot></slot>`}};p.styles=[s],e([o({attribute:"post-id"})],p.prototype,"postId",void 0),p=e([d("shreddit-post-flair")],p);
//# sourceMappingURL=pdp-post-client-js-45a25bae.js.map