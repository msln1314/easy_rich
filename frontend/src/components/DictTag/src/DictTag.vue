<script lang="tsx">
import { defineComponent, PropType, ref } from 'vue'
import { ElTag } from 'element-plus'
import { selectDictLabel, DictDetail } from '@/utils/dict'
import { useDictStore } from '@/store/modules/dict'

export default defineComponent({
  name: 'DictTag',
  props: {
    type: {
      type: String as PropType<string>,
      required: true
    },
    value: {
      type: [String, Number, Boolean] as PropType<string | number | boolean>,
      required: true
    }
  },
  setup(props) {
    const dictData = ref<DictDetail>()
    const getOptions = async (dict_type) => {
      const dictStore = useDictStore()
      const dictOptions = await dictStore.getDictObj([dict_type])
      if (!dictOptions[dict_type]) {
        return []
      }
      return dictOptions[dict_type]
    }

    const getDictObj = async (dictType: string, value: string) => {
      const dictOptions = await getOptions(dictType)
      dictOptions.forEach((dict: DictDetail) => {
        if (dict.value == value) {
          if (dict.color_type + '' === 'primary' || dict.color_type + '' === 'default') {
            dict.color_type = ''
          }
          dictData.value = dict
        }
      })
    }
    const rederDictTag = () => {
      if (!props.type) {
        return null
      }
      // 解决自定义字典标签值为零时标签不渲染的问题
      if (props.value === undefined || props.value === null) {
        return null
      }
      getDictObj(props.type, props.value.toString())
      // 添加标签的文字颜色为白色，解决自定义背景颜色时标签文字看不清的问题
      return (
        <ElTag type={dictData.value?.color_type} disableTransitions={true}>
          {dictData.value?.label || props.value}
        </ElTag>
      )
    }
    return () => rederDictTag()
  }
})
</script>
