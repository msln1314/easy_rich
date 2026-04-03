import { ElSubMenu, ElMenuItem } from 'element-plus'
import { unref } from 'vue'
import { hasOneShowingChild } from '../helper'
import { isUrl } from '@/utils/is'
import { useRenderMenuTitle } from './useRenderMenuTitle'
import { pathResolve } from '@/utils/routerHelper'
import { useDesign } from '@/hooks/web/useDesign'

const { getPrefixCls } = useDesign()
const prefixCls = getPrefixCls('submenu')

const { renderMenuTitle } = useRenderMenuTitle()

export const useRenderMenuItem = (menuMode) =>
  // allRouters: AppRouteRecordRaw[] = [],
  {
    const renderMenuItem = (routers: AppRouteRecordRaw[], parentPath = '/') => {
      if (!routers || !routers.length) return null

      return routers
        .filter((v) => !v.meta?.hidden)
        .map((v) => {
          const meta = v.meta ?? {}
          const children = v.children || []
          const hasChildren = children && children.length > 0
          const fullPath = isUrl(v.path) ? v.path : pathResolve(parentPath, v.path)

          // 如果没有子菜单，直接渲染菜单项
          if (!hasChildren) {
            return (
              <ElMenuItem index={fullPath}>
                {{
                  default: () => renderMenuTitle(meta)
                }}
              </ElMenuItem>
            )
          }

          // 有子菜单，检查是否只显示一个
          const { oneShowingChild, onlyOneChild } = hasOneShowingChild(children, v)

          if (
            oneShowingChild &&
            (!onlyOneChild?.children || onlyOneChild?.noShowingChildren) &&
            !meta?.alwaysShow
          ) {
            return (
              <ElMenuItem
                index={onlyOneChild ? pathResolve(fullPath, onlyOneChild.path) : fullPath}
              >
                {{
                  default: () => renderMenuTitle(onlyOneChild ? onlyOneChild?.meta : meta)
                }}
              </ElMenuItem>
            )
          } else {
            return (
              <ElSubMenu
                index={fullPath}
                teleported
                popperClass={unref(menuMode) === 'vertical' ? `${prefixCls}-popper--vertical` : ''}
              >
                {{
                  title: () => renderMenuTitle(meta),
                  default: () => renderMenuItem(children, fullPath)
                }}
              </ElSubMenu>
            )
          }
        })
    }

    return {
      renderMenuItem
    }
  }
