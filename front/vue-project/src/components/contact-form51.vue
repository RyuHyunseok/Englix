<template>
  <div class="contact-form51-contact1 thq-section-padding">
    <div class="thq-flex-column thq-section-max-width">
      <div class="contact-form51-section-title thq-flex-column">
        <span class="thq-body-small">
          <slot name="content2">
            <!--Default content for content2-->
            <div class="contact-form51-fragment3">
              <span class="contact-form51-text20">
                Get in touch with us today!
              </span>
            </div>
          </slot>
        </span>
        <div class="contact-form51-content">
          <h2 class="thq-heading-2">
            <slot name="heading1">
              <!--Default content for heading1-->
              <div class="contact-form51-fragment1">
                <span class="contact-form51-text18">Create</span>
              </div>
            </slot>
          </h2>
          <span class="thq-body-small contact-form51-text12">
            <slot name="content1">
              <!--Default content for content1-->
              <div class="contact-form51-fragment4">
                <span class="contact-form51-text21">
                  <span>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    <span v-html="rawfrq2"></span>
                  </span>
                  <span><span v-html="raw9sb5"></span></span>
                </span>
              </div>
            </slot>
          </span>
        </div>
      </div>
      <form class="contact-form51-form thq-flex-column">
        <div class="contact-form51-container1">
          <div class="contact-form51-input1">
            <label for="contact-form-5-first-name" class="thq-body-small">
              Title
            </label>
            <input
              type="text"
              id="contact-form-5-last-name"
              placeholder="Last Name"
              class="thq-input"
            />
          </div>
        </div>
        <div class="contact-form51-container2">
          <div class="contact-form51-input2">
            <label for="contact-form-5-last-name" class="thq-body-small">
              something
            </label>
            <input
              type="text"
              id="contact-form-5-last-name"
              placeholder="Last Name"
              class="thq-input"
            />
          </div>
        </div>
        <div class="contact-form51-container3">
          <div class="contact-form51-input3">
            <label for="contact-form-5-options" class="thq-body-small">
              Choose one topic
            </label>
            <select
              id="contact-form-5-options"
              placeholder="Select one"
              class="thq-select"
            >
              <option value="Option 1">Customer service</option>
              <option value="Option 2">Finance</option>
              <option value="Option 3">Feature request</option>
            </select>
          </div>
        </div>
        <div class="contact-form51-container4">
          <label for="contact-form-5-message" class="thq-body-small">
            Content
          </label>
          <textarea
            id="contact-form-5-message"
            rows="3"
            placeholder="Enter your message"
            class="contact-form51-textarea thq-input"
          ></textarea>
        </div>
        <div class="contact-form51-checkbox1">
          <input
            type="checkbox"
            id="contact-form-5-check"
            checked="true"
            required="true"
            class="thq-checkbox"
          />
          <label for="contact-form-5-check" class="thq-body-small">
            I accept the Terms
          </label>
        </div>
        <button type="submit" class="contact-form51-button thq-button-filled">
          <span class="thq-body-small">
            <slot name="action">
              <!--Default content for action-->
              <div class="contact-form51-fragment2">
                <span class="contact-form51-text19">Submit</span>
              </div>
            </slot>
          </span>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContactForm51',
  props: {},
  data() {
    return {
      rawfscf: ' ',
      rawlnuq: ' ',
      rawfrq2: ' ',
      raw9sb5: ' ',
    }
  },
}
</script>

<style scoped>
.contact-form51-contact1 {
  display: flex;
  position: relative;
  align-items: center;
  flex-direction: column;
}
.contact-form51-section-title {
  gap: var(--dl-space-space-unit);
  align-items: center;
}
.contact-form51-content {
  gap: var(--dl-space-space-oneandhalfunits);
  display: flex;
  align-self: stretch;
  align-items: center;
  flex-direction: column;
}
.contact-form51-form {
  gap: var(--dl-space-space-oneandhalfunits);
  width: 100%;
}
.contact-form51-container1 {
  gap: var(--dl-space-space-unit);
  flex: 0 0 auto;
  width: 100%;
  display: flex;
  align-items: flex-start;
  flex-direction: row;
}
.contact-form51-input1 {
  gap: var(--dl-space-space-halfunit);
  width: 50%;
  display: flex;
  align-self: stretch;
  align-items: flex-start;
  flex-direction: column;
}
.contact-form51-container2 {
  gap: var(--dl-space-space-unit);
  flex: 0 0 auto;
  width: 100%;
  display: flex;
  align-items: flex-start;
  flex-direction: row;
}
.contact-form51-input2 {
  gap: var(--dl-space-space-halfunit);
  width: 50%;
  display: flex;
  align-self: stretch;
  align-items: flex-start;
  flex-direction: column;
}
.contact-form51-container3 {
  flex: 0 0 auto;
  width: 50%;
  display: flex;
  align-self: flex-start;
  align-items: flex-start;
  flex-direction: column;
}
.contact-form51-input3 {
  gap: var(--dl-space-space-halfunit);
  display: flex;
  align-self: stretch;
  align-items: flex-start;
  flex-direction: column;
}
.contact-form51-container4 {
  gap: var(--dl-space-space-halfunit);
  flex: 0 0 auto;
  width: 50%;
  display: flex;
  align-self: flex-start;
  align-items: flex-start;
  flex-direction: column;
}
.contact-form51-textarea {
  width: 896px;
  height: 531px;
}
.contact-form51-checkbox1 {
  gap: var(--dl-space-space-unit);
  display: flex;
  align-self: flex-start;
  align-items: center;
}
.contact-form51-button {
  align-self: flex-start;
}
.contact-form51-fragment1 {
  display: contents;
}
.contact-form51-text18 {
  display: inline-block;
}
.contact-form51-fragment2 {
  display: contents;
}
.contact-form51-text19 {
  display: inline-block;
}
.contact-form51-fragment3 {
  display: contents;
}
.contact-form51-text20 {
  display: inline-block;
}
.contact-form51-fragment4 {
  display: contents;
}
.contact-form51-text21 {
  display: inline-block;
}
@media(max-width: 991px) {
  .contact-form51-container1 {
    gap: var(--dl-space-space-twounits);
    width: 100%;
    flex-direction: row;
  }
  .contact-form51-input1 {
    width: 50%;
  }
  .contact-form51-container2 {
    gap: var(--dl-space-space-twounits);
    width: 100%;
    flex-direction: row;
  }
  .contact-form51-input2 {
    width: 50%;
    flex-direction: column;
  }
  .contact-form51-container3 {
    gap: var(--dl-space-space-twounits);
    width: 100%;
    flex-direction: row;
  }
  .contact-form51-input3 {
    gap: var(--dl-space-space-halfunit);
    width: 50%;
    flex-direction: column;
  }
  .contact-form51-container4 {
    width: 100%;
  }
  .contact-form51-checkbox1 {
    align-self: flex-start;
  }
}
@media(max-width: 767px) {
  .contact-form51-textarea {
    flex: 1;
  }
}
@media(max-width: 479px) {
  .contact-form51-text12 {
    text-align: center;
  }
  .contact-form51-form {
    padding: var(--dl-space-space-unit);
  }
  .contact-form51-container1 {
    align-items: stretch;
    flex-direction: column;
  }
  .contact-form51-input1 {
    width: 100%;
  }
  .contact-form51-container2 {
    align-items: stretch;
    flex-direction: column;
  }
  .contact-form51-input2 {
    width: 100%;
  }
}
</style>
